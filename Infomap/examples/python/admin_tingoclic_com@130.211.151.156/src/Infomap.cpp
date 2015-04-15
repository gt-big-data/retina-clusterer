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

#include "Infomap.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <stdexcept>
#include <cstdlib>
#include "utils/Logger.h"
#include "io/Config.h"
#include "infomap/InfomapContext.h"
#include "utils/Stopwatch.h"
#include "io/ProgramInterface.h"
#include "io/convert.h"
#include "utils/FileURI.h"
#include "utils/Date.h"
#include "io/version.h"

#ifdef NS_INFOMAP
namespace infomap
{
#endif
	
void runInfomap(Config const& config)
{
	InfomapContext context(config);
	context.getInfomap()->run();
}

void runInfomap(Config const& config, Network& input, HierarchicalNetwork& output)
{
	InfomapContext context(config);
	context.getInfomap()->run(input, output);
}

std::vector<ParsedOption> getConfig(Config& conf, const std::string& flags, bool noFileIO = false)
{
	ProgramInterface api("Infomap",
			"Implementation of the Infomap clustering algorithm based on the Map Equation (see www.mapequation.org)",
			INFOMAP_VERSION);

	std::vector<std::string> optionalOutputDir; // Used if noFileIO
	// --------------------- Input options ---------------------
	if (!noFileIO)
	{
		api.addNonOptionArgument(conf.networkFile, "network_file",
				"The file containing the network data. Accepted formats: Pajek (implied by .net) and link list (.txt)");

		api.addOptionalNonOptionArguments(conf.additionalInput, "[additional input]",
				"More network layers for multiplex.", true);
	}
	else
		conf.networkFile = "no-file";

	api.addOptionArgument(conf.inputFormat, 'i', "input-format",
			"Specify input format ('pajek', 'link-list', '3gram' or 'multiplex') to override format possibly implied by file extension.", "s");

	// api.addOptionArgument(conf.withMemory, "with-memory",
	// 		"Use second order Markov dynamics and let nodes be part of different modules. Simulate memory from first-order data if not '3gram' input.", true);

	api.addOptionArgument(conf.withMemory, "overlapping",
			"Let nodes be part of different and overlapping modules. Applies to ordinary networks by first representing the memoryless dynamics with memory nodes.");

	api.addOptionArgument(conf.hardPartitions, "hard-partitions",
			"Don't allow overlapping modules in memory networks by keeping the memory nodes constrained into their physical nodes.");

	api.addOptionArgument(conf.nonBacktracking, "non-backtracking",
			"Use non-backtracking dynamics and let nodes be part of different and overlapping modules. Applies to ordinary networks by first representing the non-backtracking dynamics with memory nodes.", true);

	api.addOptionArgument(conf.parseWithoutIOStreams, "without-iostream",
			"Parse the input network data without the iostream library. Can be a bit faster, but not as robust.", true);

	api.addOptionArgument(conf.zeroBasedNodeNumbers, 'z', "zero-based-numbering",
			"Assume node numbers start from zero in the input file instead of one.");

	api.addOptionArgument(conf.includeSelfLinks, 'k', "include-self-links",
			"Include links with the same source and target node. (Ignored by default.)");

	api.addOptionArgument(conf.nodeLimit, 'O', "node-limit",
			"Limit the number of nodes to read from the network. Ignore links connected to ignored nodes.", "n", true);

	api.addOptionArgument(conf.clusterDataFile, 'c', "cluster-data",
			"Provide an initial two-level solution (.clu format).", "p", true);

	api.addOptionArgument(conf.noInfomap, "no-infomap",
			"Don't run Infomap. Useful if initial cluster data should be preserved or non-modular data printed.", true);

	// --------------------- Output options ---------------------
	api.addOptionArgument(conf.noFileOutput, '0', "no-file-output",
			"Don't print any output to file.", true);

	api.addOptionArgument(conf.printMap, "map",
			"Print the top two-level modular network in the .map format.");

	api.addOptionArgument(conf.printClu, "clu",
			"Print the top cluster indices for each node.");

	api.addOptionArgument(conf.printTree, "tree",
			"Print the hierarchy in .tree format. (default true if no other output with cluster data)");

	api.addOptionArgument(conf.printFlowTree, "ftree",
			"Print the hierarchy in .tree format and append the hierarchically aggregated network links.", true);

	api.addOptionArgument(conf.printBinaryTree, "btree",
			"Print the tree in a streamable binary format.", true);

	api.addOptionArgument(conf.printBinaryFlowTree, "bftree",
			"Print the tree including horizontal flow links in a streamable binary format.");

	api.addOptionArgument(conf.printNodeRanks, "node-ranks",
			"Print the calculated flow for each node to a file.", true);

	api.addOptionArgument(conf.printFlowNetwork, "flow-network",
			"Print the network with calculated flow values.", true);

	api.addOptionArgument(conf.printPajekNetwork, "pajek",
			"Print the parsed network in Pajek format.", true);

	api.addOptionArgument(conf.printExpanded, "expanded",
			"Print the expanded network of memory nodes if possible.", true);

	// --------------------- Core algorithm options ---------------------
	api.addOptionArgument(conf.twoLevel, '2', "two-level",
			"Optimize a two-level partition of the network.");

	bool dummyUndirected;
	api.addOptionArgument(dummyUndirected, 'u', "undirected",
			"Assume undirected links. (default)");

	api.addOptionArgument(conf.directed, 'd', "directed",
			"Assume directed links.");

	api.addOptionArgument(conf.undirdir, 't', "undirdir",
			"Two-mode dynamics: Assume undirected links for calculating flow, but directed when minimizing codelength.");

	api.addOptionArgument(conf.outdirdir, "outdirdir",
			"Two-mode dynamics: Count only ingoing links when calculating the flow, but all when minimizing codelength.", true);

	api.addOptionArgument(conf.rawdir, 'w', "rawdir",
			"Two-mode dynamics: Assume directed links and let the raw link weights be the flow.", true);

	api.addOptionArgument(conf.recordedTeleportation, 'e', "recorded-teleportation",
			"If teleportation is used to calculate the flow, also record it when minimizing codelength.", true);

	api.addOptionArgument(conf.teleportToNodes, 'o', "to-nodes",
			"Teleport to nodes instead of to links, assuming uniform node weights if no such input data.", true);

	api.addOptionArgument(conf.teleportationProbability, 'p', "teleportation-probability",
			"The probability of teleporting to a random node or link.", "f", true);

	api.addOptionArgument(conf.selfTeleportationProbability, 'y', "self-link-teleportation-probability",
			"Additional probability of teleporting to itself. Effectively increasing the code rate, generating more and smaller modules.", "f", true);

	api.addOptionArgument(conf.codeRate, "code-rate",
			"Scale link flow with this value to change the cost of moving between modules. Higher for less modules.", "f", true);

	api.addOptionArgument(conf.preferredNumberOfModules, "preferred-number-of-modules",
			"Stop merge or split modules if preferred number of modules is reached.", "n", true);

	api.addOptionArgument(conf.multiplexRelaxRate, "multiplex-relax-rate",
			"The probability to relax the constraint to move only in the current layer. If negative, the inter-links have to be provided.", "f", true);

	api.addOptionArgument(conf.seedToRandomNumberGenerator, 's', "seed",
			"A seed (integer) to the random number generator.", "n");

	// --------------------- Performance and accuracy options ---------------------
	api.addOptionArgument(conf.numTrials, 'N', "num-trials",
			"The number of outer-most loops to run before picking the best solution.", "n");

	api.addOptionArgument(conf.minimumCodelengthImprovement, 'm', "min-improvement",
			"Minimum codelength threshold for accepting a new solution.", "f", true);

	api.addOptionArgument(conf.randomizeCoreLoopLimit, 'a', "random-loop-limit",
			"Randomize the core loop limit from 1 to 'core-loop-limit'", true);

	api.addOptionArgument(conf.coreLoopLimit, 'M', "core-loop-limit",
			"Limit the number of loops that tries to move each node into the best possible module", "n", true);

	api.addOptionArgument(conf.levelAggregationLimit, 'L', "core-level-limit",
			"Limit the number of times the core loops are reapplied on existing modular network to search bigger structures.", "n", true);

	api.addOptionArgument(conf.tuneIterationLimit, 'T', "tune-iteration-limit",
			"Limit the number of main iterations in the two-level partition algorithm. 0 means no limit.", "n", true);

	api.addOptionArgument(conf.minimumRelativeTuneIterationImprovement, 'U', "tune-iteration-threshold",
			"Set a codelength improvement threshold of each new tune iteration to 'f' times the initial two-level codelength.", "f", true);

	api.addOptionArgument(conf.fastCoarseTunePartition, 'C', "fast-coarse-tune",
			"Try to find the quickest partition of each module when creating sub-modules for the coarse-tune part.", true);

	api.addOptionArgument(conf.alternateCoarseTuneLevel, 'A', "alternate-coarse-tune-level",
			"Try to find different levels of sub-modules to move in the coarse-tune part.", true);

	api.addOptionArgument(conf.coarseTuneLevel, 'S', "coarse-tune-level",
			"Set the recursion limit when searching for sub-modules. A level of 1 will find sub-sub-modules.", "n", true);

	api.addIncrementalOptionArgument(conf.fastHierarchicalSolution, 'F', "fast-hierarchical-solution",
			"Find top modules fast. Use -FF to keep all fast levels. Use -FFF to skip recursive part.");

	api.addIncrementalOptionArgument(conf.lowMemoryPriority, 'l', "low-memory",
			"Prioritize memory efficient algorithms before fast. Use -ll to optimize even more, but this may give approximate results.");

	api.addOptionArgument(conf.innerParallelization, "inner-parallelization",
			"Parallelize the innermost loop for greater speed. Note that this may give some accuracy tradeoff.");

	// --------------------- Output options ---------------------
	if (!noFileIO)
	{
		api.addNonOptionArgument(conf.outDirectory, "out_directory",
				"The directory to write the results to");
	}
	else
	{
		api.addOptionalNonOptionArguments(optionalOutputDir, "[out_directory]",
				"The directory to write the results to.");
	}

	api.addIncrementalOptionArgument(conf.verbosity, 'v', "verbose",
			"Verbose output on the console. Add additional 'v' flags to increase verbosity up to -vvv.");

	api.addOptionArgument(conf.silent, "silent",
			"No output on the console.");

	api.parseArgs(flags);

	conf.parsedArgs = flags;

	if (noFileIO)
	{
		if (!optionalOutputDir.empty())
			conf.outDirectory = optionalOutputDir[0];
	}

	// Some checks
	if (*--conf.outDirectory.end() != '/')
		conf.outDirectory.append("/");

	if (conf.haveOutput() && !isDirectoryWritable(conf.outDirectory))
		throw FileOpenError(io::Str() << "Can't write to directory '" <<
				conf.outDirectory << "'. Check that the directory exists and that you have write permissions.");

	return api.getUsedOptionArguments();
}

void initBenchmark(const Config& conf, const std::string& flags)
{
	std::string networkName = FileURI(conf.networkFile).getName();
	std::string logFilename = io::Str() << conf.outDirectory << networkName << ".tsv";
	Logger::setBenchmarkFilename(logFilename);
	std::ostringstream logInfo;
	logInfo << "#benchmark for '" << flags << "'";
	Logger::benchmark(logInfo.str(), 0, 0, 0, 0, true);
	Logger::benchmark("elapsedSeconds\ttag\tcodelength\tnumTopModules\tnumNonTrivialTopModules\ttreeDepth",
			0, 0, 0, 0, true);
	// (todo: fix problem with initializing same static file from different functions to simplify above)
	Log() << "(Writing benchmark log to '" << logFilename << "'...)\n";
}

Config init(const std::string& flags)
{
	Config conf;
	try
	{
		std::vector<ParsedOption> parsedFlags = getConfig(conf, flags, true);

		Log::init(conf.verbosity, conf.silent, conf.verboseNumberPrecision);

		Log() << "=======================================================\n";
		Log() << "  Infomap v" << INFOMAP_VERSION << " starts at " << Date() << "\n";
		if (!parsedFlags.empty()) {
			for (unsigned int i = 0; i < parsedFlags.size(); ++i)
				Log() << (i == 0 ? "  -> Configuration: " : "                    ") << parsedFlags[i] << "\n";
		}
		Log() << "  -> Use " << (conf.isUndirected()? "undirected" : "directed") << " flow and " <<
			(conf.isMemoryNetwork()? "2nd" : "1st") << " order Markov dynamics";
		if (conf.useTeleportation())
			Log() << " with " << (conf.recordedTeleportation ? "recorded" : "unrecorded") << " teleportation to " <<
			(conf.teleportToNodes ? "nodes" : "links");
		Log() << "\n";
		Log() << "=======================================================\n";

		conf.adaptDefaults();
	}
	catch (std::exception& e)
	{
		std::cerr << e.what() << std::endl;
	}

	return conf;
}

int run(Network& input, HierarchicalNetwork& output)
{
	try
	{
		runInfomap(input.config(), input, output);
	}
	catch (std::exception& e)
	{
		std::cerr << e.what() << std::endl;
		return 1;
	}
	return 0;
}

int run(const std::string& flags)
{
	Date startDate;
	Config conf;
	try
	{
		std::vector<ParsedOption> parsedFlags = getConfig(conf, flags);

		Log::init(conf.verbosity, conf.silent, conf.verboseNumberPrecision);

		Log() << "=======================================================\n";
		Log() << "  Infomap v" << INFOMAP_VERSION << " starts at " << Date() << "\n";
		Log() << "  -> Input network: " << conf.networkFile << "\n";
		Log() << "  -> Output path:   " << conf.outDirectory << "\n";
		if (!parsedFlags.empty()) {
			for (unsigned int i = 0; i < parsedFlags.size(); ++i)
				Log() << (i == 0 ? "  -> Configuration: " : "                    ") << parsedFlags[i] << "\n";
		}
		Log() << "  -> Use " << (conf.isUndirected()? "undirected" : "directed") << " flow and " <<
			(conf.isMemoryNetwork()? "2nd" : "1st") << " order Markov dynamics";
		if (conf.useTeleportation())
			Log() << " with " << (conf.recordedTeleportation ? "recorded" : "unrecorded") << " teleportation to " <<
			(conf.teleportToNodes ? "nodes" : "links");
		Log() << "\n";
		Log() << "=======================================================\n";

		if (conf.benchmark)
			initBenchmark(conf, flags);

		conf.adaptDefaults();

		runInfomap(conf);

	}
	catch (std::exception& e)
	{
		std::cerr << e.what() << std::endl;
		return EXIT_FAILURE;
	}

	ASSERT(NodeBase::nodeCount() == 0); //TODO: Not working with OpenMP
//	if (NodeBase::nodeCount() != 0)
//		Log() << "Warning: " << NodeBase::nodeCount() << " nodes not deleted!\n";


	Log() << "===================================================\n";
	Log() << "  Infomap ends at " << Date() << "\n";
	Log() << "  (Elapsed time: " << (Date() - startDate) << ")\n";
	Log() << "===================================================\n";

	return 0;
}

#ifndef AS_LIB
int main(int argc, char* argv[])
{
	std::ostringstream args("");
	for (int i = 1; i < argc; ++i)
		args << argv[i] << (i + 1 == argc? "" : " ");

	return run(args.str());
}
#endif

#ifdef NS_INFOMAP
}
#endif
