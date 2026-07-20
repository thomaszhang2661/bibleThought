# 3. Organizing: Separable, Single-Threaded Leadership

Working Backwards
## ** 3**

## ** Organizing**

### ** Separable, Single-Threaded Leadership**

* Why coordination increases and productivity decreases as organizations grow. How Amazon combated this tendency by shifting to “separable teams with single-threaded leadership.” Why creating an organization of such teams can take time, especially in a large enterprise. How to untangle dependencies so teams can work independently.*

* * *

* “The best way to fail at inventing something is by making it somebody’s part-time job.”[1](text00025.html#note13a)*

* Scene: A conference room. Jeff and several S-Team members sit across the table from the leadership team of a large Amazon business unit, including its VP, two other VPs who report to her, and several of their directors. It’s their quarterly business review, and they’re discussing an initiative that has been stuck in “Status Red” for the past two quarters. Someone asks, “What blockers are stopping you from making progress?”*

DIRECTOR X (* the most knowledgeable person for the new initiative* ): As you know, this project has many moving parts. We’ve identified five unsolved issues so far that are slowing us down. They are—

JEFF (* interrupting* ): Before we get to those issues, would someone please tell me who’s the most senior single-threaded leader for this initiative?

BUSINESS UNIT VP (* after an uncomfortably long pause* ): I am.

JEFF: But you’re in charge of the whole business unit. I want you focused on your whole group’s performance, and that includes a lot more than this one initiative.

VP 1 (* trying to take one for his team* ): That would be me, then.

JEFF: So, this is all that you and your team work on every day?

VP 1: Well, no. The only person working on it full time is one of our product managers, but we have lots of other people helping part time.

JEFF (* impatient now* ): Does a PM have all the skills, authority, and people on their team to get this done?

VP 1: Not really, no, which is why we plan to hire a director to head it up.

JEFF: How many phone screens and in-house interviews have you conducted so far for this new director?

VP 1: Well, it’s not an open position yet. We still need to complete the job description. So the answer is, zero.

JEFF: Then we’re kidding ourselves. This initiative won’t go “green” until the new leader is in place. That is the real roadblock this initiative is facing. Let’s remove that one first.

* VP 1 dashes off a terse email to head recruiter titled, “Open director role for project X leader . . .”*

* * *

Speed, or more accurately velocity, which measures both speed and direction, matters in business. With all other things being equal, the organization that moves faster will innovate more, simply because it will be able to conduct a higher number of experiments per unit of time. Yet many companies find themselves struggling against their own bureaucratic drag, which appears in the form of layer upon layer of permission, ownership, and accountability, all working against fast, decisive forward progress.

We are often asked how Amazon has managed to buck that trend by innovating so rapidly, especially across so many businesses—online retail, cloud computing, digital goods, devices, cashierless stores, and many more—while growing from fewer than ten employees to nearly one million. How has the company managed to stay nimble, not stuck struggling to find common ground, as happens with most companies of such size?

The answer lies in an Amazon innovation called “single-threaded leadership,” in which a single person, unencumbered by competing responsibilities, owns a single major initiative and heads up a separable, largely autonomous team to deliver its goals. In this chapter we’ll explain what these terms mean, how they came to be, and why they lie at the heart of the Amazon approach to innovation and high-velocity decision-making.

The single-threaded leadership model emerged at the tail end of a long, zigzag journey of well-informed trial and error. We asked ourselves a difficult question, then responded with bold critical thinking, experimentation, and relentless self-critique that helped us double down on successful ideas and jettison the failures. You won’t find an “aha moment” in this chapter. The path from that first hard question to single-threaded leadership took almost a decade, in large part because it required that we first untangle our monolithic software architecture and the organizational structures that had grown alongside it, then replace both, step by step, with systems designed to support rapid innovation.

### ** Growth Multiplied Our Challenges**

First, a bit of background. From 1997 through 2001, Amazon’s revenue grew more than twenty-one-fold from $148 million to over $3.1 billion.[2](text00025.html#note14a) Growth of the number of employees, customers, and pretty much every other measurement had similar trajectories. Innovations were being rolled out at a furious pace too. Amazon rapidly transformed from a small company that sold only books—and only in the United States—into a multinational company with logistics operations in five countries, selling almost anything that one could buy online.

During this phase, we became aware of another, less positive trend: our explosive growth was slowing down our pace of innovation. We were spending more time coordinating and less time building. More features meant more software, written and supported by more software engineers, so both the code base and the technical staff grew continuously. Software engineers were once free to modify any section of the entire code base to independently develop, test, and immediately deploy any new features to the website. But as the number of software engineers grew, their work overlapped and intertwined until it was often difficult for teams to complete their work independently.

Each overlap created one kind of* dependency* , which describes something one team needs but can’t supply for itself. If my team’s work requires effort from yours—whether it’s to build something new, participate, or review—you’re one of my dependencies. Conversely, if your team needs something from mine, I’m a dependency of yours.

Managing dependencies requires coordination—two or more people sitting down to hash out a solution—and coordination takes time. As Amazon grew, we realized that despite our best efforts, we were spending too much time coordinating and not enough time building. That’s because, while the growth in employees was linear, the number of their possible lines of communication grew exponentially. Regardless of what form it takes—and we’ll get into the different forms in more detail shortly—every dependency creates drag. Amazon’s growing number of dependencies delayed results, increased frustration, and disempowered teams.

### ** Dependencies—A Practical Example**

Let me take you back to March 1998, when I (Colin) started working at Amazon, to show how dependencies had already proliferated. At that time, the company had two large corporate divisions, one for business and one for product development. The business division was organized into operating groups defined by business function—retail, marketing, product management, fulfillment, supply chain, customer service, and so on. Each of the operating groups on the business side would request technical resources from the product development department, mainly software engineers and a small team of technical program managers (TPMs), which included me.

I got a taste of Amazon’s dependency problem in my first week on the job. Our group, led by Kim Rachmeler, was responsible for project and program management for large initiatives that required coordination of activities across multiple teams in order to achieve a key business goal. Projects this group ran included launching our music (CDs) and video (VHS/DVD) businesses, launching new websites in the United Kingdom and Germany, and some other large, internal projects.

My first assignment was to work on the Amazon Associates Program, which to date had not received much attention from the product development team. This program allowed third parties, commonly referred to as affiliates, to place links to Amazon products on their websites. For example, a site about mountain climbing might include a curated list of recommended mountain-climbing books with links to Amazon. When a visitor clicked on one of the links on the affiliate website, they were taken to the book detail page on the Amazon site. If the visitor bought that product, the owner of the affiliate website would earn a fee—known as a referral fee. Amazon was one of the pioneers in affiliate marketing and, when I got involved, we were still trying to figure out exactly what we had with this new program and how big it could become. Although it was growing, it was not widely viewed as core to the business. I guess that’s why I, as the new guy, got the assignment.

As I learned more about the Associates Program, I quickly saw that this had the potential to be a very lucrative business. At the time there were already 30,000 affiliates, and the program was growing fast. The affiliates had been creative with a very basic set of tools we had given them and were driving an ever-growing percentage of overall traffic and sales for Amazon. I believed the Associates Program could become an even bigger contributor to the business, but we would have to make several changes to it to realize its huge potential.

#### Preparing to Dive In

My first task was to manage an initiative to improve a nuts-and-bolts aspect of the program: the process we used to track and pay referral fees. At the time, we paid a referral fee only on the specific item that the affiliate website linked to. We wanted to change the program to pay referral fees on all purchases a visitor made in that shopping session. We did this because associate links were sending many customers to Amazon who didn’t purchase the recommended item but did decide to order something else during their visit. So compensating the associates for those purchases seemed only fair—it would strengthen our relationship with them, and it would encourage them to link to Amazon even more. It did not sound like a particularly complicated task. My initial assessment of the project was that we’d quickly make the minor changes to the website software and database to implement this feature, but the majority of the effort would be in the reporting, accounting, and payment software changes, and in the marketing and communication work to announce the feature to our affiliates.

Wrong. That is when I experienced firsthand the extent of dependencies at Amazon—in this case, technical dependencies. At that time, Amazon’s website software was monolithic, meaning that its functionality resided in a single massive executable program named Obidos. Its namesake is a village in Brazil along the fastest stretch of the Amazon River. As Obidos grew in size and complexity to support an ever-expanding suite of features and functionality, it began to exhibit the flip side of that once-cheerful analogy. Obidos is the fastest part of the river because it’s also the narrowest. Our entire website still flowed through one huge, growing block of code that presented a steadily rising barrier of dependencies. Obidos had become, in effect, Amazon’s bottleneck.

#### Technical Dependency Number One: Gotchas in Shared Code

Each team whose features also connected to creating a product page, putting the product in the shopping cart, finalizing an order, tracking a return, and so on represented a technical dependency for the Associates team. We had to coordinate every small step with each team because a single mistake on our part could affect their work or, even more catastrophically, could introduce a bug that would take the whole website down. Similarly, we had to dedicate our own time to reviewing* their* changes in this part of the code to ensure that our own functions were not impacted.

#### Technical Dependency Number Two: Protectors of the Database

Software code was not the only kind of technical dependency that we faced. We also needed to make changes to the underlying relational database (a database structured to recognize relations among stored information such as customers, orders, and shipments) upon which all of Amazon’s operations depended. The database was named acb, short for amazon.com books. If acb were ever to go down, the majority of the company’s operations would stop—no shopping, no orders, no fulfillment—until we could roll back the change and restart.

As a vital safeguard, a steering group had been set up to review every proposed change to acb, approve the proposal (or reject it), and then figure out the best time to implement it. This group was known colloquially, and accurately, as “DB Cabal” and comprised three senior executives—the CTO, the head of the Database Administration team, and the head of the Data team.

The Cabal reviewers were understandably protective of acb and did a good job at overseeing this important company asset. Anyone who wanted to make a change to acb would have to undergo an intimidating, if well-intentioned, design review. Given the tangled state of our technical architecture, the stakes were high and many things could go wrong, so we needed these skillful, cautious gatekeepers.

To gain their approval, you would have to demonstrate that the proposed change was low risk, the design was sound, and the payoff worth it. At the end of the review, the Cabal might approve the request or require some changes. If the latter, you would have to make the modifications, get back in the queue, and return for another review. The cycle time was maddeningly slow since this august body generally met only a few times each month, and because there were lots of other groups queueing with their own changes.

The project did launch successfully. But I noticed that in the areas where we controlled our own destiny—that is, the reporting, accounting, and payment changes, as well as our marketing plan—we were able to move fast. And in the areas where we had to make very minor changes to Obidos and acb, we moved painfully slowly. Why was that? Dependencies.

The variations in technical dependencies are endless, but each one binds teams more tightly together, turning a rapid sprint into a stumbling sack race where only the most coordinated will cross the finish line. When a software architecture includes a large number of technical dependencies, it is said to be* tightly coupled* , a bad thing that frustrates all involved when you are trying to double and triple the size of the software team. Amazon’s code had been designed in such a way that it became more tightly coupled over time.

### ** Organizational Dependencies**

Our organizational chart created extra work in a similar fashion, forcing teams to slog through layers of people to secure project approval, prioritization, and allocation of shared resources that were required to deliver a project. These organizational dependencies were just as debilitating as the technical ones.

The org chart had ballooned as we created teams for each new product category, geographic location, and function (e.g., Consumer Electronics, Amazon Japan, Graphic Design). When the company was smaller, you could enlist help or check for possible conflicts by just asking around—everyone often knew each other fairly well. At scale, the same task became long and laborious. You’d have to figure out who you needed to talk to, whether their office was in your building, and who they reported to. Maybe you’d track them down yourself, but more often you’d have to ask your manager, who in turn would ask their managers or their peers—and every step took time. Success connected you with some person (or their manager) you’d ask to listen to your pitch and commit resources to your project. They would often be doing the same thing at the same time for their own projects. In any case, they might be reluctant to slow themselves down on your behalf. You often had to do this several times for a given project, and often without success.

If your team had the resources other people needed, such requests could also come your way—sometimes many in a single week. You had to balance each one against the priorities you already had, then decide which (if any) you could support based on your own best judgment about their merits. To get a sense of how much drag these escalating organizational dependencies were adding to the average Amazon project, you had to multiply that effort as much as five or ten times. Just like our software, many of our org structures had become tightly coupled and were holding us back.

Too much of any kind of dependency not only slows down the pace of innovation but also creates a dispiriting second-order effect: disempowered teams. When a team is tasked with solving a particular problem and is judged by their solution, they should expect to have the tools and authority to complete the job. Their success should be a source of team pride. But Amazon’s tightly coupled software architecture and org structure too often made owners heavily dependent on outside teams, over whom they had little influence. Few teams were fully in control of their own destiny, and many were frustrated by the slow pace of delivery that was beyond their control. Disempowered workers increasingly became discouraged, unable to pursue innovative ideas in the face of so much structural resistance.

### ** Better Coordination Was the Wrong Answer**

Resolving a dependency usually requires coordination and communication. And when your dependencies keep growing, requiring more and more coordination, it’s only natural to try speeding things up by improving your communication. There are countless approaches to managing cross-team coordination, ranging from formalized practices to hiring dedicated coordinators—and it seemed as though we looked at them all.

At last we realized that all this cross-team communication didn’t really need refinement at all—it needed elimination. Where was it written in stone that every project had to involve so many separate entities? It wasn’t just that we had had the wrong solution in mind; rather, we’d been trying to solve the wrong problem altogether. We didn’t yet have the new solution, but we finally grasped the true identity of our problem: the ever-expanding cost of coordination among teams. This change in our thinking was of course nudged along by Jeff. In my tenure at Amazon I heard him say many times that if we wanted Amazon to be a place where builders can build, we needed to eliminate communication, not encourage it. When you view effective communication across groups as a “defect,” the solutions to your problems start to look quite different from traditional ones. He suggested that each software team should build and clearly document a set of application program interfaces (APIs) for all their systems/services. An API is a set of routines, protocols, and tools for building software applications and defining how software components should interact. In other words, Jeff’s vision was that we needed to focus on loosely coupled interaction via machines through well-defined APIs rather than via humans through emails and meetings. This would free each team to act autonomously and move faster.

### ** NPI—An Early Response to Organizational Dependencies**

Meanwhile, we faced no shortage of good business ideas. Indeed, we had many more ideas than we could support or execute—we could only take on a few big projects each quarter. Trying to prioritize which ones to pursue drove us crazy. We needed a way to ensure that our scarce resources, which mostly meant the software engineering teams, were working on the initiatives that would make the biggest impact to the business.

This gave rise to a process called New Project Initiatives (NPI), whose job was global prioritization. Not global in the sense of geographic expansion, but rather in comparing every project under consideration to decide which ones were worthy of doing immediately and which ones could wait. Such global prioritization proved to be very hard indeed. Which is more important, launching a costsaving project for fulfillment centers, adding a feature that might boost sales in the apparel category, or cleaning up old code we cannot do without to extend its practical life? There were so many unknowns and so many long-term projections to compare. Could we be sure of the extent of the cost savings? Did we know how much sales might rise with this new feature in the expected case? How could we estimate the financial payback of the restructured code, or the cost of an unknown number of outages if the old code began to fail? Every project carried risks, and most competed for the same set of scarce resources.

#### Force-Ranking Our Options

NPI was our best solution at the time for ranking our global options intelligently and picking the winners. No one liked it, but it was a necessary evil given our organization then.

Here’s how NPI worked: Once every quarter, teams submitted projects they thought were worth doing that would require resources from outside their own team—which basically meant almost every project of reasonable size. It took quite a bit of work to prepare and submit an NPI request. You needed a “one-pager”; a written summary of the idea; an initial rough estimate of which teams would be impacted; a consumer adoption model, if applicable; a P&L; and an explanation of why it was strategically important for Amazon to embark on the initiative immediately. Just proposing the idea represented a resource-intensive undertaking.

A small group would screen all the NPI submissions. A project could be cut in the first round if it wasn’t thoroughly explained, didn’t address a core company goal, didn’t represent an acceptable cost/benefit ratio, or obviously wouldn’t make the cut. The more promising ideas would move to the next round for a more detailed technical and financial scoping exercise. This step typically happened in real time in a conference room where a leader from each major area could review the project submission, ask any clarifying questions, and provide an estimate on how many resources from their area would be required to complete the project as stated. Usually 30 or 40 attendees were on hand to review a full list of projects, which made for long, long meetings—yuck.

Afterward, the smaller NPI core group would true up the resource and payback estimates, then decide which projects would actually go forward. After that group met, every project team leader would receive an email about their submission that came in one of three forms. From best to worst they were:

“Congratulations, your project has been approved! The other teams you need to help complete your project are ready to get started too.”

“The bad news is that your project was not chosen, but the good news is that none of the approved NPI projects require work from you.”

“We’re sorry that none of your projects were approved and you were probably counting on them to hit your team goals. There are, however, approved NPI projects for other teams that require resources from you. You must fully staff those NPI projects before staffing any of your other internal projects. Best of luck.”

#### Choosing Our Priorities

A lot of NPI projects were presented with large error bars—that is, an unhelpfully broad range of the potential costs and of the predicted return. “We anticipate this feature will generate between $4 million on the low side and $20 million on the high side and expect it will take 20 to 40 person-months to develop.” It’s not easy to compare projects with estimates like that.

The toughest job for many project teams was to accurately predict consumer behavior. Time and time again, we learned that consumers would behave in ways we hadn’t imagined during the development phase—especially for brand-new features or products. Even the most rigorous models we used to predict consumer adoption could be well off the mark, leading to long, vigorous debates that never quite felt conclusive. (See, for example, our story of the Fire Phone in the[introduction to part two](text00013.html#Page_155) . It’s not like we thought, “Here’s a dud, but we’re going to launch it anyway.” We had high expectations for this product in which we had invested a great deal of time and money!)

In an effort to improve our assumptions, we established a feedback loop to measure how well a team’s estimates matched its eventual results, adding another layer of accountability. Jeff Wilke stashed away paper copies of approved NPI proposals so he could check the predictions against actual results later. The added transparency and accountability helped bring team estimates closer to reality, but ultimately not close enough. A year or more could pass between the first presentation and measurable results, which is a long time to wait in order to learn what adjustments are needed.

All in all, the NPI process was not beloved. If you mention NPI to any Amazonian who went through it, you’re likely to get a grimace and maybe a horror story or two. Sometimes you got lucky, your project was approved, and you could move forward smoothly enough. Too often, however, your plans were thwarted. Instead of doing vital work on something you owned, you’d be assigned to support another team’s project while still taking care of everything that was left on your plate. “Getting NPI’d,” as we called it, meant that your team was literally getting nothing for something.

The NPI process was deflating for morale. But figuring out how to “boost morale” is not Amazonian. Other companies have morale-boosting projects and groups with names like “Fun Club” and “Culture Committee.” They view morale as a problem to be solved by company-sponsored entertainment and social interaction. Amazon’s approach to morale was to attract world-class talent and create an environment in which they had maximum latitude to invent and build things to delight customers—and you can’t do that if every quarter some faceless process like NPI smites your best ideas. In chapter six, we discuss Amazon’s belief that focusing on controllable input metrics instead of output metrics drives meaningful growth. Morale is, in a sense, an output metric, whereas freedom to invent and build is an input metric. If you clear the impediment to building, morale takes care of itself.

Our question was, “How do we do that?” It’s not that the participants in the NPI arena—or the DB Cabal for that matter—fell short or had nefarious motives. They were all top-notch, talented, hardworking people who were swimming against a riptide of dependencies. If you’re faced with a challenge that’s growing exponentially, meeting it head-on with equal but opposing force just locks you into exponentially growing cost—a dead-end strategy. We needed to find some way to stem the tide of challenges, and we finally realized that the most effective way to do that was to recognize the assumption we’d been operating under was incorrect. Amazon ultimately invented its way around the problem by cutting off dependencies at the source.

### ** First Proposed Solution: Two-Pizza Team**

Seeing that our best short-term solutions would not be enough, Jeff proposed that instead of finding new and better ways to manage our dependencies, we figure out how to remove them. We could do this, he said, by reorganizing software engineers into smaller teams that would be essentially autonomous, connected to other teams only loosely, and only when unavoidable. These largely independent teams could do their work in parallel. Instead of coordinating better, they could coordinate less and build more.

Now came the hard part—how exactly could we implement such a tectonic shift? Jeff assigned CIO Rick Dalzell to figure it out. Rick solicited ideas from people throughout the company and synthesized them, then came back with a clearly defined model that people would talk about for years to come: the* two-pizza team* , so named because the teams would be no larger than the number of people that could be adequately fed by two large pizzas. With hundreds of these two-pizza teams eventually in place, Rick believed that we would innovate at a dazzling pace. The experiment would begin in the product development organization and, if it worked, would spread throughout the rest of the company. He laid out the defining characteristics, workflow, and management as follows.

A two-pizza team will:
- ** Be small.** No more than ten people.
- ** Be autonomous.** They should have no need to coordinate with other teams to get their work done. With the new service-based software architecture in place, any team could simply refer to the published application programming interfaces (APIs) for other teams. (More on this new software architecture to follow.)
- ** Be evaluated by a well-defined “fitness function.”** This is the sum of a weighted series of metrics. Example: a team that is in charge of adding selection in a product category might be evaluated on:
a) how many new distinct items were added for the period (50 percent weighting)

b) how many units of those new distinct items were sold (30 percent weighting)

c) how many page views those distinct items received (20 percent weighting)

- ** Be monitored in real time.** A team’s real-time score on its fitness function would be displayed on a dashboard next to all the other two-pizza teams’ scores.
- ** Be the business owner.** The team will own and be responsible for all aspects of its area of focus, including design, technology, and business results. This paradigm shift eliminates the all-too-often heard excuses such as, “We built what the business folks asked us to, they just asked for the wrong product,” or “If the tech team had actually delivered what we asked for and did it on time, we would have hit our numbers.”
- ** Be led by a multidisciplined top-flight leader.** The leader must have deep technical expertise, know how to hire world-class software engineers and product managers, and possess excellent business judgment.
- ** Be self-funding.** The team’s work will pay for itself.
- ** Be approved in advance by the S-Team.** The S-Team must approve the formation of every two-pizza team.

As with any major innovation at Amazon, this plan was merely the beginning. Some of its tenets endured, some evolved, and some perished over the course of several years. The most important of these adaptations are worth exploring here in more detail.

#### Tearing Down Monoliths

“Be autonomous.” Sounds simple, doesn’t it? In fact, it would be hard to overstate the effort we expended to free these teams from the constraints that bound them so tightly at the beginning. The effort would necessitate major changes to the way we wrote, built, tested, and deployed our software, how we stored our data, and how we monitored our systems to keep them running twenty-four hours a day, seven days a week. The details are numerous and interesting in their own right, but most fall well beyond the scope of this book. One major effort is worth recounting in some detail, however, because it was both vital and extremely difficult for us to achieve.

Just as two-pizza teams replaced a single large organization with something faster and more flexible, a comparable reorganization was overdue for much of the Amazon software architecture to enable us to achieve Rick’s “be autonomous” vision. In a 2006 interview by Jim Gray, Amazon CTO Werner Vogels recalled another watershed moment:

We went through a period of serious introspection and concluded that a service-oriented architecture would give us the level of isolation that would allow us to build many software components rapidly and independently. By the way, this was way before service-oriented was a buzzword. For us service orientation means encapsulating the data with the business logic that operates on the data, with the only access through a published service interface. No direct database access is allowed from outside the service, and there’s no data sharing among the services.[3](text00025.html#note15a)

That’s a lot to unpack for non–software engineers, but the basic idea is this: If multiple teams have direct access to a shared block of software code or some part of a database, they slow each other down. Whether they’re allowed to change the way the code works, change how the data are organized, or merely build something that uses the shared code or data, everybody is at risk if anybody makes a change. Managing that risk requires a lot of time spent in coordination. The solution is to encapsulate, that is, assign ownership of a given block of code or part of a database to one team. Anyone else who wants something from that walled-off area must make a well-documented service request via an API.[4](text00025.html#note16a)

Think of it like a restaurant. If you are hungry, you don’t walk into the kitchen and fix what you want. You ask for a menu, then choose an item from it. If you want something that is not on that menu, you can ask the waiter, who will send a request to the cook. But there is no guarantee you’ll get it. What happens inside the walled-off area in question is completely up to the single team that owns it, so long as they don’t change how information can be exchanged. If change becomes necessary, the owners publish a revised set of rules—a new menu, if you will—and all those who rely on them are notified.

This new system greatly improved upon the free-for-all it replaced. For the purposes of this book, suffice it to say that implementing this improvement meant replacing Obidos, acb, and many other key pieces of our software infrastructure piece by piece while it was still running our business nonstop. This required a major investment in development resources, systems architecture planning, and great care to ensure that the monolith continued to stand until its last surviving function had been replaced by a service. The rolling regeneration of the way we built and deployed technology was a bold move, an expensive investment that stretched over several years of intensive and delicate work.

Today the advantages of a microservices-based architecture are well understood, and the approach has been adopted by many tech companies. The benefits include improved agility, developer productivity, scalability, and a better ability to resolve and recover from outages and failures. In addition, with microservices, it becomes possible to establish small, autonomous teams that can assume a level of ownership of their code that isn’t possible with a monolithic approach. The switch to microservices removed the shackles that had prevented the Amazon software teams from moving fast, and enabled the transition to small, autonomous teams.

#### The First Autonomous Teams

Autonomous teams are built for speed. When they are aligned toward a common destination, they can go a long way in a short time. But when they are poorly aligned, the team can veer far off course just as quickly. So they need to be pointed in the right direction and have the tools to quickly course-correct when warranted. That’s why, before any proposed two-pizza team was approved, they had to meet with Jeff and their S-Team manager—often more than once—to discuss the team’s composition, charter, and fitness function.

For instance, the Inventory Planning team would convene with Jeff, Jeff Wilke, and me to ensure that they were meeting the following criteria:
1. The team had a well-defined purpose. For example, the team intends to answer the question, “How much inventory should Amazon buy of a given product and when should we buy it?”
1. The boundaries of ownership were well understood. For example, the team asks the Forecasting team what the demand will be for a particular product at a given time, and then uses their answer as an input to make a buying decision.
1. The metrics used to measure progress were agreed upon. For example, In-stock Product Pages Displayed divided by Total Product Pages Displayed, weighted at 60 percent; and Inventory Holding Cost, weighted at 40 percent.

Importantly, the specifics of how the proposed team would go about achieving its goal were not discussed at the meeting. That was the team’s role to figure out for themselves.

These meetings were a classic example of the Dive Deep leadership principle. I participated in every one of the Fitness Function alignment meetings for the first set of two-pizza teams, which owned things like Forecasting, Customer Reviews, and Customer Service Tools. We questioned every metric from every angle, probing how those data would be collected and how the results would be used to drive the team accurately toward its goals. These meetings clearly established expectations and confirmed the team’s readiness. Just as importantly, they also built up trust between Jeff and the new team, reinforcing their autonomy—and therefore their velocity.

We started with a small number of two-pizza teams so that we could learn what worked and refine the model before widespread adoption. One significant lesson became clear fairly early: each team started out with its own share of dependencies that would hold them back until eliminated, and eliminating the dependencies was hard work with little to no immediate payback. The most successful teams invested much of their early time in removing dependencies and building “instrumentation”—our term for infrastructure used to measure every important action—before they began to innovate, meaning, add new features.

For example, the Picking team owned software that directed workers in the fulfillment centers where to find items on the shelves. They spent much of their first nine months systematically identifying and removing dependencies from upstream areas, like receiving inventory from vendors, and downstream areas, like packing and shipping. They also built systems to track every important event that happened in their area at a detailed, real-time level. Their business results didn’t improve much while they did so, but once they had removed dependencies, built their fitness function, and instrumented their systems, they became a strong example of how fast a two-pizza team could innovate and deliver results. They became advocates of this new way of working.

Other teams, however, put off doing the unglamorous work of removing their dependencies and instrumenting their systems. Instead, they focused too soon on the flashier work of developing new features, which enabled them to make some satisfying early progress. Their dependencies remained, however, and the continuing drag soon became apparent as the teams lost momentum.

A well-instrumented two-pizza team had another powerful benefit. They were better at course correcting—detecting and fixing mistakes as they arose. In the 2016 shareholder letter, even though he wasn’t explicitly talking about two-pizza teams, Jeff suggested that “most decisions should probably be made with somewhere around 70% of the information you wish you had. If you wait for 90%, in most cases, you’re probably being slow. Plus, either way, you need to be good at quickly recognizing and correcting bad decisions. If you’re good at course correcting, being wrong may be less costly than you think, whereas being slow is going to be expensive for sure.”[5](text00025.html#note17a)

Good examples like the Picking team demonstrated how longterm thinking, in the form of their up-front investments, generated compound returns over time. Later teams followed their lead. Sometimes it’s best to start slow in order to move fast.

While it would be nice to trust that a swarm of loosely coupled, autonomous teams will always make the best tactical choices to deliver the company’s larger strategic objectives, that’s sometimes wishful thinking—even with the best of teams. The OP1 process we described in chapter one still framed the autonomy of these teams by aligning them with company strategy, giving them their initial bearing toward upcoming yearly targets.

And we came to realize that other limits to autonomy would also need to remain, with each team still tied to others by varying levels of dependency. While each two-pizza team crafted its own product vision and development roadmap, unavoidable dependencies could arise in the form of cross-functional projects or top-down initiatives that spanned multiple teams. For example, a two-pizza team working on picking algorithms for the fulfillment centers might also be called upon to add support for robotics being implemented to move products around the warehouse.

We found it helpful to think of such cross-functional projects as a kind of tax, a payment one team had to make in support of the overall forward progress of the company. We tried to minimize such intrusions but could not avoid them altogether. Some teams, through no fault of their own, found themselves in a higher tax bracket than others. The Order Pipeline and Payments teams, for example, had to be involved in almost every new initiative, even though it wasn’t in their original charters.

### ** Some Challenges Still Remained**

Two-pizza teams were a much-talked-about topic at Amazon, but as originally defined, they didn’t spread throughout the company as completely as some other new ideas had. While they showed great potential to improve the way Amazon worked, they also exhibited some shortcomings that limited their success and broader applicability.

#### Two-Pizza Teams Worked Best in Product Development

We weren’t sure how far to take the two-pizza team concept, and at the beginning it was planned solely as a reorganization of product development. Seeing its early success in speeding up innovation, we wondered whether it might also work in retail, legal, HR, and other areas. The answer turned out to be no, because those areas did not suffer from the tangled dependencies that had hampered Amazon product development. Therefore, implementing two-pizza teams in those orgs would not increase speed.

#### Fitness Functions Were Actually Worse Than Their Component Metrics

Two-pizza teams had been meant to increase the velocity of product development, with custom-tailored fitness functions serving as the directional component of each team’s velocity. By pointing each team in the right direction and alerting them early if they drifted off course, fitness functions were supposed to align the team uniquely to its goals. We tried them out for more than a year, but fitness functions never really delivered on their promise for a couple of important reasons.

First, teams spent an inordinate amount of time struggling with how to construct the most meaningful fitness function. Should the formula be 50 percent for Metric A plus 30 percent for Metric B plus 20 percent for Metric C? Or should it be 45 percent for Metric A plus 40 percent for Metric B plus 15 percent for Metric C? You can imagine how easy it was to get lost in those debates. The discussions became less useful and ultimately distracting—just another argument that people needed to win.

Second, some of these overly complicated functions combined seven or more metrics, a few of which were composite numbers built from their own submetrics. When graphed over time, they might describe a trend line that went up and to the right, but what did that mean? It was often impossible to discern what the team was doing right (or wrong) and how they should respond to the trend. Also, the relative weightings could change over time as business conditions changed, obscuring historic trends altogether.

We eventually reverted to relying directly on the underlying metrics instead of the fitness function. After experimenting over many months across many teams, we realized that as long as we did the up-front work to agree on the specific metrics for a team, and we agreed on specific goals for each input metric, that was sufficient to ensure the team would move in the right direction. Combining them into a single, unifying indicator was a very clever idea that simply didn’t work.

#### Great Two-Pizza Team Leaders Proved to Be Rarities

The original idea was to create a large number of small teams, each under a solid, multidisciplined, frontline manager and arranged collectively into a traditional, hierarchical org chart. The manager would be comfortable mentoring and diving deep in areas ranging from technical challenges to financial modeling and business performance. Although we did identify a few such brilliant managers, they turned out to be notoriously difficult to find in sufficient numbers, even at Amazon. This greatly limited the number of two-pizza teams we could effectively deploy, unless we relaxed the constraint of forcing teams to have direct-line reporting to such rare leaders.

We found instead that two-pizza teams could also operate successfully in a matrix organization model, where each team member would have a solid-line reporting relationship to a functional manager who matched their job description—for example, director of software development or director of product management—and a dotted-line reporting relationship to their two-pizza manager. This meant that individual two-pizza team managers could lead successfully even without expertise in every single discipline required on their team. This functional matrix ultimately became the most common structure, though each two-pizza team still devised its own strategies for choosing and prioritizing its projects.

#### Sometimes You Need More Than Two Pizzas

We all agreed at the outset that a smaller team would work better than a larger one. But we later came to realize that the biggest predictor of a team’s success was not whether it was small but whether it had a leader with the appropriate skills, authority, and experience to staff and manage a team whose sole focus was to get the job done.

Now free of its initial size limits, the two-pizza team clearly needed a new name. Nothing catchy came to mind, so we leaned into our geekdom and chose the computer science term “single-threaded,” meaning you only work on one thing at a time. Thus, “single-threaded leaders” and “separable, single-threaded teams” were born.

### ** Bigger and Better Still—The Single-Threaded Leader**

Even though the two-pizza model hadn’t taken root as quickly as we’d planned, nor had it spread across the organization as far as we’d hoped, the experiment showed enough promise that Jeff and the S-Team had the patience and discipline to stick with it. We learned as we went, adapting and refining the idea of two-pizza teams until, in the end, we had something far more capable.

What was originally known as a two-pizza team leader (2PTL) evolved into what is now known as a single-threaded leader (STL). The STL extends the basic model of separable teams to deliver their key benefits at any scale the project demands. Today, despite their initial success, few people at Amazon still talk about two-pizza teams.

We say that the STL is bigger and better, but better than what? Certainly it’s an improvement on the two-pizza team it evolved from, but is it better than other alternatives too? To answer that question, let’s look at a more common approach to developing something new.

Typically an executive, assigned to drive some innovation or initiative, would turn to one of his reports—possibly a director or senior manager—who might have responsibility for five of the executive’s 26 total initiatives. The executive would ask the director to identify one of those direct reports—let’s say a project manager—who would add the project to their to-do list. The PM, in turn, would prevail upon an engineering director to see if one of their dev teams could squeeze the work into their dev schedule. Amazon’s SVP of Devices, Dave Limp, summed up nicely what might happen next: “The best way to fail at inventing something is by making it somebody’s part-time job.”[6](text00025.html#note18a)

Amazon learned the hard way how this lack of a single-threaded leader could hinder them in getting new initiatives off the ground. One example is Fulfillment by Amazon (FBA). Initially known as Self-Service Order Fulfillment (SSOF), its purpose was to offer Amazon’s warehouse and shipping services to merchants. Rather than handling the storing, picking, packing, and shipping themselves, the merchants would send products to Amazon, and we would handle the logistics from there. The executives in the retail and operations teams thought this was a big, interesting idea, but for well over a year it did not gain significant traction. It was always “coming soon,” but it never actually arrived.

Finally, in 2005, Jeff Wilke asked Tom Taylor, then a VP, to drop his other responsibilities and gave him approval to hire and staff a team. Only then did SSOF take off, eventually morphing into Fulfillment by Amazon. FBA launched in September 2006 and became a huge success. Third-party sellers loved it because, by offering them warehouse space for their products, Amazon turned warehousing into a variable cost for them instead of a fixed cost. FBA also enabled third-party sellers to reap the benefits of participating in Prime, which in turn improved the customer experience for buyers. As Jeff said in a letter to shareholders, “In just the last quarter of 2011, Fulfillment by Amazon shipped tens of millions of items on behalf of sellers.”[7](text00025.html#note19a)

The leaders who had been trying to get this service off the ground before Tom Taylor took it over were exceptionally capable people, but while they were tending to all their other responsibilities, they just didn’t have the bandwidth to manage the myriad details FBA entailed. FBA would have been, at best, much slower and more difficult to launch if Jeff Wilke hadn’t freed up Tom to focus on nothing but this one project. The single-threaded leader concept hadn’t yet been formalized at Amazon, but Tom became an important forerunner.

The other crucial component of the STL model is a* separable, single-threaded team* being run by a single-threaded leader like Tom. As Jeff Wilke explains, “Separable means almost as separable organizationally as APIs are for software. Single-threaded means they don’t work on anything else.”[8](text00025.html#note20a)

Such teams have clear, unambiguous ownership of specific features or functionality and can drive innovations with a minimum of reliance or impact upon others. Appointing a single-threaded leader is necessary but not sufficient. It’s much more than a simple org chart change. Separable, single-threaded teams have fewer organizational dependencies than conventional teams. They clearly demarcate the boundaries of what they own and where the interests of other teams begin and end. As former Amazon VP Tom Killalea aptly observed, a good rule of thumb to see if a team has sufficient autonomy is deployment—can the team build and roll out their changes without coupling, coordination, and approvals from other teams? If the answer is no, then one solution is to carve out a small piece of functionality that can be autonomous and repeat.

A single-threaded leader can head up a small team, but they can also lead the development of something as large as Amazon Echo or Digital Music. For example, with Amazon Echo and Alexa, were it not for the fact that Amazon VP Greg Hart was assigned to be the single-threaded leader, there might have been one person in charge of hardware and another in charge of software for all of Amazon’s devices—but no one whose job it was to create and launch Amazon Echo and Alexa as a whole. On the contrary, a single-threaded leader of Amazon Echo and Alexa had the freedom and autonomy to assess the novel product problems that needed to be solved, decide what and how many teams they needed, how the responsibilities should be divided up among the teams, and how big each team should be. And, crucially, since the technical dependencies problem had been solved, that leader no longer had to check with a prohibitively large number of people for each software change they needed to make.

### ** The Payback**

It took us a while to arrive at the approach of single-threaded leaders and separable, single-threaded teams, and we went through a number of solutions along the way that ultimately didn’t last—like NPIs and two-pizza teams. But it was worth it, because where we landed was an approach to innovation that is so fundamentally sound and adaptable that it survives at Amazon to this day. This journey is also a great example of another phrase you’ll hear at Amazon: be stubborn on the vision but flexible on the details.

The STL delivers high-velocity innovation, which in turn makes Amazon nimble and responsive even at its now-massive scale. Free of the hindrance of excess dependencies, innovators at every level can experiment and innovate faster, leading to more sharply defined products and a higher level of engagement for their creators. Ownership and accountability are much easier to establish under the STL model, keeping teams properly focused and accurately aligned with company strategies. While all these positive outcomes were possible before the first autonomous single-threaded team was created, now they have become the natural and expected consequence of this very Amazonian model for innovation.
