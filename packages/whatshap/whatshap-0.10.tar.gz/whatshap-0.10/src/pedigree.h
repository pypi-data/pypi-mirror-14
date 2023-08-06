#ifndef PEDIGREE_H
#define PEDIGREE_H

#include <iostream>
#include <unordered_map>

/*
 * how to use:
 * - build up a pedigree by adding individuals and their genotypes with addIndividual(),
 * - then add the relationship between them with addRelationship().
 */
class Pedigree {
public:
	Pedigree();
	typedef std::array<unsigned int, 3> triple_entry_t;
	//typedef std::array<std::vector<unsigned int>, 3> genotype_entry_t;

	// add genotypes of a single individual
	void addIndividual(unsigned int individual, std::vector<unsigned int> genotypes);

	// add a relationship (a mother/father/child triple)
	void addRelationship(unsigned int mother, unsigned int father, unsigned int child);

	size_t size() const {
		return individuals.size();
	}
	std::vector<triple_entry_t> triples;
	//std::vector<genotype_entry_t> triple_genotypes;
	std::vector<unsigned int> individuals;
	std::unordered_map<unsigned int, std::vector<unsigned int>> genotypes_map;
private:
	
	// maps individual ids to genotypes

};

#endif
