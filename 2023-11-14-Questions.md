# Food Web Project

## Species Attributes

- Species_ID: a unique identifier for each species.
- Life_span: a constant that defines the average life span of each species.
- Full_energy: a constant that defines the maximum energy level of each species.
- Mature_stage: an interval that individuals of this species can reproduce.
- Maximum_reproduction: a constant that defines the maximum number of offspring that an individual can produce.
- Reproduction_cost: a constant that defines the energy cost of reproduction.

## Individual Attributes

- Type_ID: the same as Species_ID, but for individuals.
- Remaining_life: a constant which is randomly generated from the species Life_span.
- Energy: a constant which is randomly generated from the species Full_energy.
- Is_Mature: a boolean value that indicates whether the individual is mature or not.
- Mating_Rank: a float number between 0 and 1, which is randomly generated from a uniform distribution. 
It represents the score of an individual in the mating pool. The higher the score, the more likely the individual will be chosen as a mate.
- Reproduction_ability: an integer between 0 and Maximum_reproduction.
- Number_of_offspring: an integer between 0 and Reproduction_ability.
- Reproduction_cost: a constant which is the same as the species Reproduction_cost.
- Natural_death_rate: an interval that the probability of an individual dying of natural causes is randomly generated from.
- (x,y): the location of the individual in the grid.
- Is_Dead: a boolean value that indicates whether the individual is dead or not.

## Interaction

Let's say species A = Rabbit, species B = Fox, species C = Wolf.

- What will happen when two individuals of the same species meet?
- What will happen when Species A meets Species B? If B kills A, how much energy will B gain? How much energy will B lose during the fight?
- What will happen when Species A meets Species C? 
- What will happen when Species B meets Species C? 
- What will happen when 5 individuals of Species A meet a single individual of Species B?
- What will happen when two different species are very near to each other? Will the weaker one escape? How much is the escape distance and probability?
- How do two individuals choose each other as mates? Do they choose the closest one? Or the one with the highest Mating_Rank? Or the one with the highest energy level?
- Where will the offspring be born? At the location of the mother? Or at a random location nearby?
- How do the lowest species in the food chain interact with plants? What is the growth rate of plants?
- Does the environment have an impact on the interaction? 
For example, if the environment is a desert, will the growth rate of plants be lower? Or if the environment is a forest, will the growth rate of plants be higher?
- Speaking of the search radius, should we define the speed and the search radius of each species?
- Does the speed related to individual's current energy level and age?
- etc.

## It is quite complicated, isn't it? 😭










