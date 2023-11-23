## That's Sick!
###### A disease simulation by Loes Oldhoff

Welcome to 'That's  Sick!', a pygame simulation of the well-described SIR model, of disease spreading in a population.

The SIR model assumes a population of entities, that regularly interact with each other on a random basis. An entity can be in one of three states:

* **S**usceptible
* **I**nfected
* **R**esistant (or Recovered or Removed)

In this simulation, these entities and interactions are visualised on a screen, with entities moving around in real time through a 2D plane.
Entities change colour depending on their SIR-state, and can interact accordingly. Infected individuals have a chance to infect any Susceptible
individuals in close proximity to them, and will after some time transition to the Resistant state. 

In order for this simulation to work, a few Infected entities need to be present at the start.

If you have acquired this code, chances are you are a bio-informatics student at the Hanze University of applied sciences. 
If this is the case, you are hereby invited to take and edit this code to your hearts content. Scattered throughout this project 
are #TODO prompts, with ideas on how this model can be improved. But naturally, creativity is encouraged and appreciated. Don't
be afraid to break things, you can always re-clone. 





