/**********************************************************************************

 Infomap software package for multi-level network clustering

 Copyright (c) 2013, 2014 Daniel Edler, Martin Rosvall
 
 For more information, see <http://www.mapequation.org>
 

 This file is part of Infomap software package.

 Infomap software package is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Infomap software package is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with Infomap software package.  If not, see <http://www.gnu.org/licenses/>.

**********************************************************************************/


#include "Network.h"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>

#include "../io/convert.h"
#include "../io/SafeFile.h"
#include "../utils/FileURI.h"
#include "../utils/Logger.h"

#ifdef NS_INFOMAP
namespace infomap
{
#endif

using std::make_pair;

void Network::readInputData(std::string filename)
{
	if (filename.empty())
		filename = m_config.networkFile;
	FileURI networkFilename(filename, false);
	std::string format = m_config.inputFormat;

	if (format == "")
	{
		std::string type = networkFilename.getExtension();
		if (type == "net")
			format = "pajek";
		else if (type == "txt")
			format = "link-list";
	}
	if (format == "")
		throw UnknownFileTypeError("No known input format specified or implied by file extension.");

	if (format == "pajek")
		parsePajekNetwork(filename);
	else if (format == "link-list")
		parseLinkList(filename);
	else
		throw UnknownFileTypeError("No known input format specified.");
}

void Network::parsePajekNetwork(std::string filename)
{
	if (m_config.parseWithoutIOStreams)
	{
		parsePajekNetworkWithoutIOStreams(filename);
		return;
	}

	Log() << "Parsing " << (m_config.isUndirected() ? "undirected" : "directed") << " network from file '" <<
			filename << "'... " << std::flush;

	SafeInFile input(filename.c_str());

	// Parse the vertices and return the line after
	std::string line = parseVertices(input);

	std::istringstream ss;
	std::string buf;
	ss.str(line);
	ss >> buf;
	if(buf != "*Edges" && buf != "*edges" && buf != "*Arcs" && buf != "*arcs") {
		throw FileFormatError("The first line (to lower cases) after the nodes doesn't match *edges or *arcs.");
	}
	if (m_config.parseAsUndirected() && (buf == "*Arcs" || buf == "*arcs"))
		Log() << "\n --> Notice: Links marked as directed in pajek file but parsed as undirected.\n";

	// Read links in format "from to weight", for example "1 3 2" (all integers) and each undirected link only ones (weight is optional).
	while(!std::getline(input, line).fail())
	{
		if (line.length() == 0)
			continue;

		unsigned int n1, n2;
		double weight;
		parseLink(line, n1, n2, weight);

		addLink(n1, n2, weight);
	}

	Log() << "done!" << std::endl;

	finalizeAndCheckNetwork();
}

void Network::parsePajekNetworkWithoutIOStreams(std::string filename)
{
	Log() << "Parsing " << (m_config.isUndirected() ? "undirected" : "directed") << " network from file '" <<
				filename << "' (without iostreams)... " << std::flush;
	FILE* file;
	file = fopen(filename.c_str(), "r");
	if (file == NULL)
		throw FileOpenError(io::Str() << "Error opening file '" << filename << "'");

	const int LINELENGTH = 511;
	char line[LINELENGTH];
	char *cptr;

	while (m_numNodesFound == 0)
	{
		if (fgets(line , LINELENGTH , file) == NULL)
			throw FileFormatError("Can't find a correct line that defines the beginning of the node section.");
		if (strncmp(line, "*", 1) != 0)
			continue;

		cptr = strchr(line, ' ');
		if (cptr == NULL)
			throw FileFormatError("Can't find a correct line that defines the beginning of the node section.");
		m_numNodesFound = atoi(++cptr);
	}

	bool checkNodeLimit = m_config.nodeLimit > 0;
	m_numNodes = checkNodeLimit ? m_config.nodeLimit : m_numNodesFound;

	m_nodeNames.resize(m_numNodes);
	m_nodeWeights.assign(m_numNodes, 1.0);
	m_sumNodeWeights = 0.0;

	int next = fgetc(file);
	ungetc(next, file);
	if (next == '*') // Short pajek version (no nodes defined), set node number as name
	{
		char nameBuff[16];
		for (unsigned int i = 0; i < m_numNodes; ++i)
		{
			m_nodeWeights[i] = 1.0;
			snprintf(nameBuff, 16, "%d", i+1);
			m_nodeNames[i] = std::string(nameBuff);
		}
		m_sumNodeWeights = m_numNodes * 1.0;
	}
	else
	{
		char *first;
		char *last;
		// Read node names, assuming order 1, 2, 3, ...
		for(unsigned int i = 0; i < m_numNodes; ++i)
		{
			if (fgets (line , LINELENGTH , file) == NULL)
				throw FileFormatError("Can't read enough nodes.");

			first = strchr(line, '\"')+1;
			last = strrchr(line, '\"');
			if(last > first)
			{
				size_t len = (size_t)(last - first);
				m_nodeNames[i] = std::string(first, len);
			}
			else
			{
				throw FileFormatError(io::Str() << "Can't read \"name\" of node " << (i+1) << ".");
			}

			double nodeWeight = strtod(++last, NULL);
			if (nodeWeight < 1e-10)
				nodeWeight = 1.0;

			m_sumNodeWeights += nodeWeight;
			m_nodeWeights[i] = nodeWeight;
		}

		if (m_config.nodeLimit > 0 && m_numNodes < m_numNodesFound)
		{
			unsigned int surplus = m_numNodesFound - m_numNodes;
			for (unsigned int i = 0; i < surplus; ++i)
			{
				if (fgets (line , LINELENGTH , file) == NULL)
					throw FileFormatError("The specified number of nodes is more than the number of lines that can be read.");
			}
		}
	}


	if (fgets (line , LINELENGTH , file) == NULL)
		throw FileFormatError("Can't find a correct line that defines the beginning of the edge section.");
	if (strncmp(line, "*", 1) != 0)
		throw FileFormatError("Can't find a correct line that defines the beginning of the edge section.");

	if (m_config.parseAsUndirected() && (strncmp(line, "*Arcs", 5) == 0 || strncmp(line, "*arcs", 5) == 0))
		Log() << "\n --> Notice: Links marked as directed in pajek file but parsed as undirected.\n";


	// Read links in format "from to weight", for example "1 3 2" (all integers) and each undirected link only ones (weight is optional).
	while(fgets (line , LINELENGTH , file) != NULL)
	{
		unsigned int n1, n2;
		double weight;
		parseLink(line, n1, n2, weight);

		addLink(n1, n2, weight);
	}

	fclose(file);

	Log() << "done!" << std::endl;

	finalizeAndCheckNetwork();
}

void Network::parseLinkList(std::string filename)
{
	if (m_config.parseWithoutIOStreams)
	{
		parseLinkListWithoutIOStreams(filename);
		return;
	}

	string line;
	string buf;
	SafeInFile input(filename.c_str());
	Log() << "Parsing " << (m_config.directed ? "directed" : "undirected") << " link list from file '" <<
			filename << "'... " << std::flush;

	std::istringstream ss;


	// Read links in format "from to weight", for example "1 3 2" (all integers) and each undirected link only ones (weight is optional).

	while(!std::getline(input, line).fail())
	{
		if (line.length() == 0 || line[0] == '#')
			continue;

		unsigned int n1, n2;
		double weight;
		parseLink(line, n1, n2, weight);

		addLink(n1, n2, weight);
	}

	Log() << "done!" << std::endl;

	finalizeAndCheckNetwork();
}

void Network::parseLinkListWithoutIOStreams(std::string filename)
{
	Log() << "Parsing " << (m_config.isUndirected() ? "undirected" : "directed") << " link list from file '" <<
					filename << "' (without iostreams)... " << std::flush;
	FILE* file;
	file = fopen(filename.c_str(), "r");
	if (file == NULL)
		throw FileOpenError(io::Str() << "Error opening file '" << filename << "'");

	const int LINELENGTH = 63;
	char line[LINELENGTH];


	// Read links in format "from to weight", for example "1 3 2" (all integers) and each undirected link only ones (weight is optional).
	while(fgets (line , LINELENGTH , file) != NULL)
	{
		unsigned int n1, n2;
		double weight;
		parseLink(line, n1, n2, weight);

		addLink(n1, n2, weight);
	}

	fclose(file);

	Log() << "done! ";

	finalizeAndCheckNetwork();
}

//////////////////////////////////////////////////////////////////////////////////////////
//
//  HELPER METHODS
//
//////////////////////////////////////////////////////////////////////////////////////////

std::string Network::parseVertices(std::ifstream& file)
{
	std::string line;

	while(!std::getline(file, line).fail())
	{
		if (line.length() == 0 || line[0] == '#')
			continue;
		if (line[0] == '*')
			break;

	}
	if (line.length() == 0 || line[0] != '*')
		throw FileFormatError("No matching header for vertices found.");

	return parseVertices(file, line);
}

std::string Network::parseVertices(std::ifstream& file, std::string header)
{
	std::istringstream ss;
	std::string buf;
	ss.str(header);
	ss >> buf;
	if(buf == "*Vertices" || buf == "*vertices" || buf == "*VERTICES") {
		if (!(ss >> m_numNodesFound))
			throw BadConversionError(io::Str() << "Can't parse an integer after '" << buf <<
					"' as the number of nodes.");
	}
	else {
		throw FileFormatError(io::Str() << "The header '" << header << "' doesn't match *Vertices (case insensitive).");
	}

	if (m_numNodesFound == 0)
		throw FileFormatError("The number of vertices cannot be zero.");

	bool checkNodeLimit = m_config.nodeLimit > 0;
	m_numNodes = checkNodeLimit ? m_config.nodeLimit : m_numNodesFound;

	m_nodeNames.resize(m_numNodes);
	m_nodeWeights.assign(m_numNodes, 1.0);
	m_sumNodeWeights = 0.0;

	std::string line;
	char next = file.peek();
	if (next == '*') // Short pajek version (no nodes defined), set node number as name
	{
		for (unsigned int i = 0; i < m_numNodes; ++i)
		{
			m_nodeWeights[i] = 1.0;
			m_nodeNames[i] = io::stringify(i+1);
		}
		m_sumNodeWeights = m_numNodes * 1.0;
	}
	else
	{
		// Read node names, assuming order 1, 2, 3, ... (or 0, 1, 2, ... if zero-based node numbering)
		for (unsigned int i = 0; i < m_numNodes; ++i)
		{
			unsigned int id = 0;
			if (!(file >> id) || id != static_cast<unsigned int>(i + m_indexOffset))
			{
				throw BadConversionError(io::Str() << "Couldn't parse line " << (i + m_indexOffset + 1) << ". Should begin with node number " << (i + m_indexOffset) <<
						((m_indexOffset == 1 && id == i)? ".\nBe sure to use zero-based node numbering if the node numbers start from zero." : "."));
			}
			// Read the rest of the line
			std::getline(file,line);
			unsigned int nameStart = line.find_first_of("\"");
			unsigned int nameEnd = line.find_last_of("\"");
			string name;
			double nodeWeight = 1.0;
			if(nameStart < nameEnd) {
				name = string(line.begin() + nameStart + 1, line.begin() + nameEnd);
				line = line.substr(nameEnd + 1);
				ss.clear();
				ss.str(line);
			}
			else {
				ss.clear();
				ss.str(line);
				ss >> buf; // Take away the index from the stream
				ss >> name; // Extract the next token as the name assuming no spaces
			}
			ss >> nodeWeight; // Extract the next token as node weight. If failed, the old value (1.0) is kept.
			m_sumNodeWeights += nodeWeight;
			m_nodeWeights[i] = nodeWeight;
			m_nodeNames[i] = name;
		}

		if (m_config.nodeLimit > 0 && m_numNodes < m_numNodesFound)
		{
			unsigned int surplus = m_numNodesFound - m_numNodes;
			for (unsigned int i = 0; i < surplus; ++i)
				std::getline(file, line);
		}
	}
	// Return the line after the vertices
	std::getline(file, line);
	return line;
}

void Network::parseLink(const std::string& line, unsigned int& n1, unsigned int& n2, double& weight)
{
	m_extractor.clear();
	m_extractor.str(line);
	if (!(m_extractor >> n1 >> n2))
		throw FileFormatError(io::Str() << "Can't parse link data from line '" << line << "'");
	(m_extractor >> weight) || (weight = 1.0);
	n1 -= m_indexOffset;
	n2 -= m_indexOffset;
}

void Network::parseLink(char line[], unsigned int& n1, unsigned int& n2, double& weight)
{
	char *cptr;
	cptr = strtok(line, " \t"); // Get first non-whitespace character position
	if (cptr == NULL)
		throw FileFormatError(io::Str() << "Can't parse link data from line '" << line << "'");
	n1 = atoi(cptr); // get first connected node
	cptr = strtok(NULL, " \t"); // Get second non-whitespace character position
	if (cptr == NULL)
		throw FileFormatError(io::Str() << "Can't parse link data from line '" << line << "'");
	n2 = atoi(cptr); // get the second connected node
	cptr = strtok(NULL, " \t"); // Get third non-whitespace character position
	if (cptr != NULL)
		weight = atof(cptr); // get the link weight
	else
		weight = 1.0;
	n1 -= m_indexOffset;
	n2 -= m_indexOffset;
}



bool Network::addLink(unsigned int n1, unsigned int n2, double weight)
{
	++m_numLinksFound;

	if (m_config.nodeLimit > 0 && (n1 >= m_config.nodeLimit || n2 >= m_config.nodeLimit))
		return false;

	if (n2 == n1)
	{
		++m_numSelfLinksFound;
		if (!m_config.includeSelfLinks)
			return false;
		++m_numSelfLinks;
		m_totalSelfLinkWeight += weight;
	}
	else if (m_config.parseAsUndirected() && n2 < n1) // minimize number of links
		std::swap(n1, n2);

	m_maxNodeIndex = std::max(m_maxNodeIndex, std::max(n1, n2));
	m_minNodeIndex = std::min(m_minNodeIndex, std::min(n1, n2));

	insertLink(n1, n2, weight);

	return true;
}


bool Network::insertLink(unsigned int n1, unsigned int n2, double weight)
{
	++m_numLinks;
	m_totalLinkWeight += weight;

	// Aggregate link weights if they are definied more than once
	LinkMap::iterator firstIt = m_links.lower_bound(n1);
	if (firstIt != m_links.end() && firstIt->first == n1) // First linkEnd already exists, check second linkEnd
	{
		std::pair<std::map<unsigned int, double>::iterator, bool> ret2 = firstIt->second.insert(std::make_pair(n2, weight));
		if (!ret2.second)
		{
			ret2.first->second += weight;
			++m_numAggregatedLinks;
			--m_numLinks;
			return false;
		}
	}
	else
	{
		m_links.insert(firstIt, std::make_pair(n1, std::map<unsigned int, double>()))->second.insert(std::make_pair(n2, weight));
	}

	return true;
}

void Network::finalizeAndCheckNetwork(bool printSummary, unsigned int desiredNumberOfNodes)
{
	if (m_links.empty())
		throw InputDomainError("No links added!");

	// If no nodes defined
	if (m_numNodes == 0)
		m_numNodes = m_numNodesFound = m_maxNodeIndex + 1;

	if (desiredNumberOfNodes != 0)
	{
		if (!m_nodeNames.empty() && desiredNumberOfNodes != m_nodeNames.size())
			throw InputDomainError("Can't change the number of nodes in networks with a specified number of nodes.");
		m_numNodes = desiredNumberOfNodes;
	}

	unsigned int zeroMinusOne = 0;
	--zeroMinusOne;
	if (m_maxNodeIndex == zeroMinusOne)
		throw InputDomainError(io::Str() << "Integer overflow, be sure to use zero-based node numbering if the node numbers start from zero.");
	if (m_maxNodeIndex >= m_numNodes)
		throw InputDomainError(io::Str() << "At least one link is defined with node numbers that exceeds the number of nodes.");
	if (m_minNodeIndex == 1 && m_config.zeroBasedNodeNumbers)
		Log() << "(Warning: minimum link index is one, check that you don't use zero based numbering if it's not true.) ";

	if (m_addSelfLinks)
		zoom();

	initNodeDegrees();

	if (printSummary)
		printParsingResult();
}

void Network::zoom()
{
	unsigned int numNodes = m_numNodes;
	std::vector<unsigned int> nodeOutDegree(numNodes, 0);
	std::vector<double> sumLinkOutWeight(numNodes, 0.0);
	std::map<unsigned int, double> dummy;
	std::vector<std::map<unsigned int, double>::iterator> existingSelfLinks(numNodes, dummy.end());

	for (LinkMap::iterator linkIt(m_links.begin()); linkIt != m_links.end(); ++linkIt)
	{
		unsigned int linkEnd1 = linkIt->first;
		std::map<unsigned int, double>& subLinks = linkIt->second;
		for (std::map<unsigned int, double>::iterator subIt(subLinks.begin()); subIt != subLinks.end(); ++subIt)
		{
			unsigned int linkEnd2 = subIt->first;
			double linkWeight = subIt->second;
			++nodeOutDegree[linkEnd1];
			if (linkEnd1 == linkEnd2)
			{
				// Store existing self-link to aggregate additional weight
				existingSelfLinks[linkEnd1] = subIt;
//				sumLinkOutWeight[linkEnd1] += linkWeight;
			}
			else
			{
				if (m_config.isUndirected())
				{
					sumLinkOutWeight[linkEnd1] += linkWeight * 0.5; // Why half?
					sumLinkOutWeight[linkEnd2] += linkWeight * 0.5;
					++nodeOutDegree[linkEnd2];
				}
				else
				{
					sumLinkOutWeight[linkEnd1] += linkWeight;
				}
			}
		}
	}

	double selfProb = m_config.selfTeleportationProbability;

	for (unsigned int i = 0; i < numNodes; ++i)
	{
		if (nodeOutDegree[i] == 0)
			continue; // Skip dangling nodes at the moment

		double selfLinkWeight = sumLinkOutWeight[i] * selfProb / (1.0 - selfProb);

		if (existingSelfLinks[i] != dummy.end()) {
			existingSelfLinks[i]->second += selfLinkWeight;
		}
		else {
			m_links[i].insert(std::make_pair(i, selfLinkWeight));
			++m_numAdditionalLinks;
		}
		m_sumAdditionalLinkWeight += selfLinkWeight;
	}

	m_numLinks += m_numAdditionalLinks;
	m_numSelfLinks += m_numAdditionalLinks;
	m_totalLinkWeight += m_sumAdditionalLinkWeight;
	m_totalSelfLinkWeight += m_sumAdditionalLinkWeight;
}

void Network::initNodeDegrees()
{
	m_outDegree.assign(m_numNodes, 0.0);
	m_sumLinkOutWeight.assign(m_numNodes, 0.0);
	m_numDanglingNodes = m_numNodes;
	for (LinkMap::iterator linkIt(m_links.begin()); linkIt != m_links.end(); ++linkIt)
	{
		unsigned int n1 = linkIt->first;
		std::map<unsigned int, double>& subLinks = linkIt->second;
		for (std::map<unsigned int, double>::iterator subIt(subLinks.begin()); subIt != subLinks.end(); ++subIt)
		{
			unsigned int n2 = subIt->first;
			double linkWeight = subIt->second;
			if (m_outDegree[n1] == 0)
				--m_numDanglingNodes;
			++m_outDegree[n1];
			m_sumLinkOutWeight[n1] += linkWeight;
			if (n1 != n2 && m_config.parseAsUndirected())
			{
				if (m_outDegree[n2] == 0)
					--m_numDanglingNodes;
				++m_outDegree[n2];
				m_sumLinkOutWeight[n2] += linkWeight;
			}
		}
	}
}

void Network::printParsingResult(bool onlySummary)
{
	bool dataModified = m_numNodesFound != m_numNodes || m_numLinksFound != m_numLinks;

	if (onlySummary)
	{
		Log() << " ==> " << getParsingResultSummary() << '\n';
		return;
	}

	if (!dataModified)
		Log() << " ==> " << getParsingResultSummary();
	else {
		Log() << " --> Found " << m_numNodesFound << io::toPlural(" node", m_numNodesFound);
		Log() << " and " << m_numLinksFound << io::toPlural(" link", m_numLinksFound) << ".";
	}

	if(m_numAggregatedLinks > 0)
		Log() << "\n --> Aggregated " << m_numAggregatedLinks << io::toPlural(" link", m_numAggregatedLinks) << " to existing links.";
	if (m_numSelfLinksFound > 0 && !m_config.includeSelfLinks)
		Log() << "\n --> Ignored " << m_numSelfLinksFound << io::toPlural(" self-link", m_numSelfLinksFound) << ".";
	unsigned int numNodesIgnored = m_numNodesFound - m_numNodes;
	if (m_config.nodeLimit > 0)
		Log() << "\n --> Ignored " << numNodesIgnored << io::toPlural(" node", numNodesIgnored) << " due to specified limit.";
	if (m_numDanglingNodes > 0)
		Log() << "\n --> " << m_numDanglingNodes << " dangling " << io::toPlural("node", m_numDanglingNodes) << " (nodes with no outgoing links).";

	if (m_numAdditionalLinks > 0)
		Log() << "\n --> Added " << m_numAdditionalLinks << io::toPlural(" self-link", m_numAdditionalLinks) << " with total weight " << m_sumAdditionalLinkWeight << ".";
	if (m_numSelfLinks > 0) {
		Log() << "\n --> " << m_numSelfLinks << io::toPlural(" self-link", m_numSelfLinks);
		Log() << " with total weight " << m_totalSelfLinkWeight << " (" << (m_totalSelfLinkWeight / m_totalLinkWeight * 100) << "% of the total link weight).";
	}

	if (dataModified) {
		Log() << "\n ==> " << getParsingResultSummary();
	}
	Log() << std::endl;
}

std::string Network::getParsingResultSummary()
{
	std::ostringstream o;
	o << m_numNodes << io::toPlural(" node", m_numNodes);
	if (!m_nodeWeights.empty() && std::abs(m_sumNodeWeights / m_numNodes - 1.0) > 1e-9)
		o << " (with total weight " << m_sumNodeWeights << ")";
	o << " and " << m_numLinks << io::toPlural(" link", m_numLinks);
	if (std::abs(m_totalLinkWeight / m_numLinks - 1.0) > 1e-9)
		o << " (with total weight " << m_totalLinkWeight << ")";
	o << ".";
	return o.str();
}


void Network::printNetworkAsPajek(std::string filename) const
{
	SafeOutFile out(filename.c_str());

	out << "*Vertices " << m_numNodes << "\n";
	if (m_nodeNames.empty()) {
		for (unsigned int i = 0; i < m_numNodes; ++i)
			out << (i+1) << " \"" << i + 1 << "\"\n";
	}
	else {
		for (unsigned int i = 0; i < m_numNodes; ++i)
			out << (i+1) << " \"" << m_nodeNames[i] << "\"\n";
	}

	out << (m_config.isUndirected() ? "*Edges " : "*Arcs ") << m_links.size() << "\n";
	for (LinkMap::const_iterator linkIt(m_links.begin()); linkIt != m_links.end(); ++linkIt)
	{
		unsigned int linkEnd1 = linkIt->first;
		const std::map<unsigned int, double>& subLinks = linkIt->second;
		for (std::map<unsigned int, double>::const_iterator subIt(subLinks.begin()); subIt != subLinks.end(); ++subIt)
		{
			unsigned int linkEnd2 = subIt->first;
			double linkWeight = subIt->second;
			out << (linkEnd1 + 1) << " " << (linkEnd2 + 1) << " " << linkWeight << "\n";
		}
	}
}

#ifdef NS_INFOMAP
}
#endif
