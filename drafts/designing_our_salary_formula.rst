Designing our Salary Formula
============================

These last weeks I have invested a lot of my time getting my head around
hiring, as we plan to onboard the next two or three employees at Tideways over
the next months. My goal is to hire highly qualified and motivated people
across all experience levels. One major part of attracting this talent besides
the actual work and company culture is obviously compensation.

I was always heavily interested in the use of a salary formula like Buffer,
Travis-CI or Gitlab have them. They seem to avoid salary differences that pit
employees against each other based soly on their negotiation skill (which is
not a primary soft skill that engineers need anyways) and against their
employer who has even more information to exploit.

But the longer you try out the mathematical salary formulas, the more random
their results feel. How can you even come up with a multipler for experience?
Finally, it seems these salary formulas are extremely high maintenance with
regard to each multipler.

This is when I found Basecamps approach, which is a refreshing new take on the
problem: They are getting salary data from a reputable third party salary
aggregator. Based on the actual real world distribution of salaries Basecamp
then just pays at the very high end for each role/experience. This system is
also automatically increasing salaries with the current market rate, which
makes it very low maintenance in updating.

Designing a "Salary Formula" for Tideways meant finding a similar provider for
Germany, which exists with `Compensation Partner
<https://www.compensation-partner.de/de/beratungsleistungen/gehaltsspiegel/ueberblick>`_.
This company provides data on the real distribution of backend and frontend
engineers based on age (proxy for experience), region, degree and level of
responsibility.

Our salary "formula" starts with the "Total Remuneration" (base salary, bonus
and benefits), using not the average but the top quartile (only 25% earn more)
value. I then applied the region adjustment percentage for Cologne, the nearest
large city to Tideways headquarter in Bonn. The average salary for a software
engineer in Cologne is a lot higher than in the average of Germany, but also
lower than Munich or Frankfurt and a few other large cities.

I then spent several days to build the first version (0.1) of our engineering
ladder with 6 experience levels. This work is based mostly on the pre-existing ladders from other
organizations such as Rent The Runway, Urban Airship and Basecamp. You can find
`these and many other engineering ladders
<https://squeakyvessel.com/2016/07/11/engineering-ladders-links-elsewhere/>`_
listed on this excellent page by Benjamin Reitzhammer. This blog post on
`designing performance management systems
<https://blog.gitprime.com/designing-performance-management-systems/>`_ helped
me with nitty gritty details defining a career ladder.

Each level on the Tideways engineering ladder is then matched to an experience
and responsibility level in the salary report. The salary report lists negative
or positive percentages to multiply the base salary with to get to the adjusted
salary for that level. Multipliers depend on company size, and I used the
factors for companies with 1-20 employees for now. For the education axis I
would always pick diploma/master for all levels, except for the entry level
Engineer I. Final values are then rounded up to the next highest hundred for
simplicity. Then I cross referenced the results with `StackOverflow Salary
Calculator <https://stackoverflow.com/jobs/salary>`_ to find out they are not
completly different.

Now when I write a job ad looking for an engineer, I can directly give
applicants a salary range that they can earn, for 2018/2019 it ranges from
42.000 to 78.000 based on their experience as defined by the ladder. 

Obviously it is not a perfect system, but there are two reasons why I think it
doesn't matter too much:

1. By using the top quartile not the average as base salary, we heavily lean
   towards higher salaries on every level by default. This accounts for small
   mistakes in the formula. Statistically speaking, applying the percentages
   onto the 75% quartile is also skewing values towards the higher end. 

2. Salary for the two highest levels are in the top 10% of engineering salaries
   in Germany, independent of company size and region according to both
   StackOverflow and Compensation Partner data, which is already good pay
   considering that we are a self funded startup with finite financial
   resources.

Using the Cologne region and the 1-20 employees company range for salary
factors makes it a bit harder for us to compete for excellent people that don't
mind working at larger companies from 20-500 employees. 

At some point we have to consider paying employees as if they worked at larger
companies in the more expensive German cities.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
