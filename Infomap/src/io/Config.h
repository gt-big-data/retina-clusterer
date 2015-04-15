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


#ifndef CONFIG_H_
#define CONFIG_H_

#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#include "../utils/Date.h"
#include "version.h"

#ifdef NS_INFOMAP
namespace infomap
{
#endif

struct Config
{
	Config()
	:	parsedArgs(""),
		networkFile(""),
	 	inputFormat(""),
	 	withMemory(false),
		hardPartitions(false),
	 	nonBacktracking(false),
	 	parseWithoutIOStreams(false),
		zeroBasedNodeNumbers(false),
		includeSelfLinks(false),
		ignoreEdgeWeights(false),
		nodeLimit(0),
	 	clusterDataFile(""),
	 	noInfomap(false),
	 	twoLevel(false),
		directed(false),
		undirdir(false),
		outdirdir(false),
		rawdir(false),
		recordedTeleportation(false),
		teleportToNodes(false),
		teleportationProbability(0.15),
		selfTeleportationProbability(-1),
		codeRate(1.0),
		preferredNumberOfModules(0),
		multiplexRelaxRate(-1),
		seedToRandomNumberGenerator(123),
		numTrials(1),
		minimumCodelengthImprovement(1.0e-10),
		minimumSingleNodeCodelengthImprovement(1.0e-16),
		randomizeCoreLoopLimit(false),
		coreLoopLimit(0),
		levelAggregationLimit(0),
		tuneIterationLimit(0),
		minimumRelativeTuneIterationImprovement(1.0e-5),
		fastCoarseTunePartition(false),
		alternateCoarseTuneLevel(false),
		coarseTuneLevel(1),
		fastHierarchicalSolution(0),
		fastFirstIteration(false),
		lowMemoryPriority(0),
		innerParallelization(false),
		outDirectory("."),
		originallyUndirected(false),
		printTree(false),
		printFlowTree(false),
		printMap(false),
		printClu(false),
		printNodeRanks(false),
		printFlowNetwork(false),
		printPajekNetwork(false),
		printBinaryTree(false),
		printBinaryFlowTree(false),
		printExpanded(false),
		noFileOutput(false),
		verbosity(0),
		verboseNumberPrecision(6),
		silent(false),
		benchmark(false),
		version(INFOMAP_VERSION)
	{
		setOptimizationLevel(1);
	}

	Config(const Config& other)
	:	parsedArgs(other.parsedArgs),
		networkFile(other.networkFile),
	 	additionalInput(other.additionalInput),
	 	inputFormat(other.inputFormat),
	 	withMemory(other.withMemory),
		hardPartitions(other.hardPartitions),
	 	nonBacktracking(other.nonBacktracking),
	 	parseWithoutIOStreams(other.parseWithoutIOStreams),
		zeroBasedNodeNumbers(other.zeroBasedNodeNumbers),
		includeSelfLinks(other.includeSelfLinks),
		ignoreEdgeWeights(other.ignoreEdgeWeights),
		nodeLimit(other.nodeLimit),
	 	clusterDataFile(other.clusterDataFile),
	 	noInfomap(other.noInfomap),
	 	twoLevel(other.twoLevel),
		directed(other.directed),
		undirdir(other.undirdir),
		outdirdir(other.outdirdir),
		rawdir(other.rawdir),
		recordedTeleportation(other.recordedTeleportation),
		teleportToNodes(other.teleportToNodes),
		teleportationProbability(other.teleportationProbability),
		selfTeleportationProbability(other.selfTeleportationProbability),
		codeRate(other.codeRate),
		preferredNumberOfModules(other.preferredNumberOfModules),
		multiplexRelaxRate(other.multiplexRelaxRate),
		seedToRandomNumberGenerator(other.seedToRandomNumberGenerator),
		numTrials(other.numTrials),
		minimumCodelengthImprovement(other.minimumCodelengthImprovement),
		minimumSingleNodeCodelengthImprovement(other.minimumSingleNodeCodelengthImprovement),
		randomizeCoreLoopLimit(other.randomizeCoreLoopLimit),
		coreLoopLimit(other.coreLoopLimit),
		levelAggregationLimit(other.levelAggregationLimit),
		tuneIterationLimit(other.tuneIterationLimit),
		minimumRelativeTuneIterationImprovement(other.minimumRelativeTuneIterationImprovement),
		fastCoarseTunePartition(other.fastCoarseTunePartition),
		alternateCoarseTuneLevel(other.alternateCoarseTuneLevel),
		coarseTuneLevel(other.coarseTuneLevel),
		fastHierarchicalSolution(other.fastHierarchicalSolution),
		fastFirstIteration(other.fastFirstIteration),
		lowMemoryPriority(other.lowMemoryPriority),
		innerParallelization(other.innerParallelization),
		outDirectory(other.outDirectory),
		originallyUndirected(other.originallyUndirected),
		printTree(other.printTree),
		printFlowTree(other.printFlowTree),
		printMap(other.printMap),
		printClu(other.printClu),
		printNodeRanks(other.printNodeRanks),
		printFlowNetwork(other.printFlowNetwork),
		printPajekNetwork(other.printPajekNetwork),
		printBinaryTree(other.printBinaryTree),
		printBinaryFlowTree(other.printBinaryFlowTree),
		printExpanded(other.printExpanded),
		noFileOutput(other.noFileOutput),
		verbosity(other.verbosity),
		verboseNumberPrecision(other.verboseNumberPrecision),
		silent(other.silent),
		benchmark(other.benchmark),
		startDate(other.startDate),
		version(other.version)
	{
	}

	Config& operator=(const Config& other)
	{
		parsedArgs = other.parsedArgs;
		networkFile = other.networkFile;
	 	additionalInput = other.additionalInput;
	 	inputFormat = other.inputFormat;
	 	withMemory = other.withMemory;
	 	hardPartitions = other.hardPartitions;
	 	nonBacktracking = other.nonBacktracking;
	 	parseWithoutIOStreams = other.parseWithoutIOStreams;
		zeroBasedNodeNumbers = other.zeroBasedNodeNumbers;
		includeSelfLinks = other.includeSelfLinks;
		ignoreEdgeWeights = other.ignoreEdgeWeights;
		nodeLimit = other.nodeLimit;
	 	clusterDataFile = other.clusterDataFile;
	 	noInfomap = other.noInfomap;
	 	twoLevel = other.twoLevel;
		directed = other.directed;
		undirdir = other.undirdir;
		outdirdir = other.outdirdir;
		rawdir = other.rawdir;
		recordedTeleportation = other.recordedTeleportation;
		teleportToNodes = other.teleportToNodes;
		teleportationProbability = other.teleportationProbability;
		selfTeleportationProbability = other.selfTeleportationProbability;
	 	codeRate = other.codeRate;
	 	preferredNumberOfModules = other.preferredNumberOfModules;
		multiplexRelaxRate = other.multiplexRelaxRate;
		seedToRandomNumberGenerator = other.seedToRandomNumberGenerator;
		numTrials = other.numTrials;
		minimumCodelengthImprovement = other.minimumCodelengthImprovement;
		minimumSingleNodeCodelengthImprovement = other.minimumSingleNodeCodelengthImprovement;
		randomizeCoreLoopLimit = other.randomizeCoreLoopLimit;
		coreLoopLimit = other.coreLoopLimit;
		levelAggregationLimit = other.levelAggregationLimit;
		tuneIterationLimit = other.tuneIterationLimit;
		minimumRelativeTuneIterationImprovement = other.minimumRelativeTuneIterationImprovement;
		fastCoarseTunePartition = other.fastCoarseTunePartition;
		alternateCoarseTuneLevel = other.alternateCoarseTuneLevel;
		coarseTuneLevel = other.coarseTuneLevel;
		fastHierarchicalSolution = other.fastHierarchicalSolution;
		fastFirstIteration = other.fastFirstIteration;
		lowMemoryPriority = other.lowMemoryPriority;
		innerParallelization = other.innerParallelization;
		outDirectory = other.outDirectory;
		originallyUndirected = other.originallyUndirected;
		printTree = other.printTree;
		printFlowTree = other.printFlowTree;
		printMap = other.printMap;
		printClu = other.printClu;
		printNodeRanks = other.printNodeRanks;
		printFlowNetwork = other.printFlowNetwork;
		printPajekNetwork = other.printPajekNetwork;
		printBinaryTree = other.printBinaryTree;
		printBinaryFlowTree = other.printBinaryFlowTree;
		printExpanded = other.printExpanded;
		noFileOutput = other.noFileOutput;
		verbosity = other.verbosity;
		verboseNumberPrecision = other.verboseNumberPrecision;
		silent = other.silent;
		startDate = other.startDate;
		version = other.version;
		return *this;
	}

	// Set all optimization options at once with different accuracy to performance trade-off
	void setOptimizationLevel(unsigned int level)
	{
		switch (level)
		{
		case 0: // full coarse-tune
			randomizeCoreLoopLimit = false;
			coreLoopLimit = 0;
			levelAggregationLimit = 0;
			tuneIterationLimit = 0;
			minimumRelativeTuneIterationImprovement = 1.0e-6;
			fastCoarseTunePartition = false;
			alternateCoarseTuneLevel = true;
			coarseTuneLevel = 3;
			break;
		case 1: // fast coarse-tune
			randomizeCoreLoopLimit = true;
			coreLoopLimit = 10;
			levelAggregationLimit = 0;
			tuneIterationLimit = 0;
			minimumRelativeTuneIterationImprovement = 1.0e-5;
			fastCoarseTunePartition = true;
			alternateCoarseTuneLevel = false;
			coarseTuneLevel = 1;
			break;
		case 2: // no tuning
			randomizeCoreLoopLimit = true;
			coreLoopLimit = 10;
			levelAggregationLimit = 0;
			tuneIterationLimit = 1;
			fastCoarseTunePartition = true;
			alternateCoarseTuneLevel = false;
			coarseTuneLevel = 1;
			break;
		case 3: // no aggregation nor any tuning
			randomizeCoreLoopLimit = true;
			coreLoopLimit = 10;
			levelAggregationLimit = 1;
			tuneIterationLimit = 1;
			fastCoarseTunePartition = true;
			alternateCoarseTuneLevel = false;
			coarseTuneLevel = 1;
			break;
		}
	}

	void adaptDefaults()
	{
		if (!haveModularResultOutput())
			printTree = true;

		originallyUndirected = isUndirected();
		if (isMemoryNetwork())
		{
			if (isMultiplexNetwork())
			{
				// Include self-links in multiplex networks as layer and node numbers are unrelated
				includeSelfLinks = true;
				if (!isUndirected())
				{
					teleportToNodes = true;
					recordedTeleportation = false;
				}
			}
			else
			{
				teleportToNodes = true;
				recordedTeleportation = false;
				if (isUndirected())
					directed = true;
			}
		}

	}

	bool isUndirected() const { return !directed && !undirdir && !outdirdir && !rawdir; }

	bool isUndirectedFlow() const { return !directed && !outdirdir && !rawdir; } // isUndirected() || undirdir

	bool printAsUndirected() const { return originallyUndirected; }

	bool parseAsUndirected() const { return originallyUndirected; }

	bool useTeleportation() const { return 	directed; }

	bool isMemoryInput() const { return inputFormat == "3gram" || inputFormat == "multiplex" || additionalInput.size() > 0; }

	bool isMemoryNetwork() const { return withMemory || nonBacktracking || isMemoryInput(); }

	bool isSimulatedMemoryNetwork() const { return (withMemory || nonBacktracking) && !isMemoryInput(); }

	bool isMultiplexNetwork() const { return inputFormat == "multiplex" || additionalInput.size() > 0; }

	bool haveOutput() const
	{
		return !noFileOutput;
	}

	bool haveModularResultOutput() const
	{
		return printTree ||
				printFlowTree ||
				printMap ||
				printClu ||
				printBinaryTree ||
				printBinaryFlowTree;
	}

	ElapsedTime elapsedTime() const { return Date() - startDate; }


	// Input
	std::string parsedArgs;
	std::string networkFile;
	std::vector<std::string> additionalInput;
	std::string inputFormat; // 'pajek', 'link-list', '3gram' or 'multiplex'
	bool withMemory;
	bool hardPartitions;
	bool nonBacktracking;
	bool parseWithoutIOStreams;
	bool zeroBasedNodeNumbers;
	bool includeSelfLinks;
	bool ignoreEdgeWeights;
	unsigned int nodeLimit;
	std::string clusterDataFile;
	bool noInfomap;

	// Core algorithm
	bool twoLevel;
	bool directed;
	bool undirdir;
	bool outdirdir;
	bool rawdir;
	bool recordedTeleportation;
	bool teleportToNodes;
	double teleportationProbability;
	double selfTeleportationProbability;
	double codeRate;
	unsigned int preferredNumberOfModules;
	double multiplexRelaxRate;
	unsigned long seedToRandomNumberGenerator;

	// Performance and accuracy
	unsigned int numTrials;
	double minimumCodelengthImprovement;
	double minimumSingleNodeCodelengthImprovement;
	bool randomizeCoreLoopLimit;
	unsigned int coreLoopLimit;
	unsigned int levelAggregationLimit;
	unsigned int tuneIterationLimit; // num iterations of fine-tune/coarse-tune in two-level partition)
	double minimumRelativeTuneIterationImprovement;
	bool fastCoarseTunePartition;
	bool alternateCoarseTuneLevel;
	unsigned int coarseTuneLevel;
	unsigned int fastHierarchicalSolution;
	bool fastFirstIteration;
	unsigned int lowMemoryPriority; // Prioritize memory efficient algorithms before fast if > 0
	bool innerParallelization;

	// Output
	std::string outDirectory;
	bool originallyUndirected;
	bool printTree;
	bool printFlowTree;
	bool printMap;
	bool printClu;
	bool printNodeRanks;
	bool printFlowNetwork;
	bool printPajekNetwork;
	bool printBinaryTree;
	bool printBinaryFlowTree; // tree including horizontal links (hierarchical network)
	bool printExpanded; // Print the expanded network of memory nodes if possible
	bool noFileOutput;
	unsigned int verbosity;
	unsigned int verboseNumberPrecision;
	bool silent;
	bool benchmark;

	// Other
	Date startDate;
	std::string version;
};

#ifdef NS_INFOMAP
}
#endif

#endif /* CONFIG_H_ */
