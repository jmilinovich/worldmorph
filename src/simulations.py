ORGANIZATION_SIM = """# Tech Company Simulation - Canva 2024

## Initial World State
Canva:
- Employees: 3,600
- Valuation: $26 billion
- Products: Design, Websites, Video, Print
- Offices: Sydney HQ + 12 global
- Revenue: $1.7 billion ARR
- Growth: 40% YoY

## Agents

### Executive Team
1. CEO Melanie Perkins
   Actions Available:
   - Set company strategy
   - Final decisions on products
   - Resource allocation
   Current Focus:
   - AI integration
   - Enterprise expansion
   - Team growth

2. Head of Product Cameron Adams
   Actions Available:
   - Product roadmap
   - Feature prioritization
   - Team structure
   Reports:
   - 8 product directors
   - 40 product managers
   - 200 designers

3. Head of Engineering
   Actions Available:
   - Technical architecture
   - Build vs buy decisions
   - Resource allocation
   Teams:
   - Frontend (120 engineers)
   - Backend (80 engineers)
   - ML/AI (40 engineers)
   - Infrastructure (30 engineers)

### Middle Management

1. Product Directors (8)
   Responsibilities:
   - Design Tools
   - Website Builder
   - Video Editor
   - Print Service
   - Enterprise
   - Mobile Apps
   - AI Features
   - Platform
   Actions:
   - Feature specs
   - Team assignments
   - Release planning

2. Engineering Managers (15)
   Teams: 10-15 engineers each
   Actions:
   - Sprint planning
   - Performance reviews
   - Technical decisions
   Focus Areas:
   - Service reliability
   - Code quality
   - Team productivity

### Individual Contributors

1. Senior Engineers (180)
   Skills:
   - Technical expertise (85-100)
   - System design (80-100)
   - Mentoring (70-100)
   Actions:
   - Code architecture
   - Technical reviews
   - Feature implementation
   
2. Mid-Level Engineers (160)
   Skills:
   - Technical expertise (60-85)
   - Implementation (70-90)
   - Collaboration (60-90)
   Actions:
   - Feature development
   - Code reviews
   - Testing

3. Junior Engineers (90)
   Skills:
   - Technical expertise (30-60)
   - Learning speed (60-90)
   - Collaboration (50-80)
   Actions:
   - Bug fixes
   - Small features
   - Testing
   Growth:
   - +1 skill per month
   - Promotion eligible: 18 months

4. Product Managers (40)
   Skills:
   - Product sense (70-100)
   - Communication (80-100)
   - Technical understanding (60-90)
   Actions:
   - Feature specs
   - Stakeholder management
   - Release planning

5. Designers (200)
   Types:
   - Product (120)
   - Visual (50)
   - UX Research (30)
   Actions:
   - Design systems
   - User flows
   - Visual assets

## Interaction Rules

1. Product Development
   - Daily standups
   - Weekly planning
   - Bi-weekly demos
   - Monthly reviews
   Process:
   - Spec review (2 days)
   - Design review (3 days)
   - Implementation (5-15 days)
   - Testing (3-5 days)
   - Release (1 day)

2. Communication Channels
   - Slack (instant)
   - Email (async)
   - JIRA (tracking)
   - Confluence (docs)
   - Zoom (meetings)

3. Release Cycle
   - Daily deployments
   - Weekly feature releases
   - Monthly major updates
   - Quarterly planning

## Time Scale
- Each tick = 1 hour
- Work day = 8 hours
- Work week = 40 hours
- Simulation runs 1 year

"""

ECONOMIC_SIM = """# Economic Policy Simulation - US Economy 2024

## Initial World State 2024
The United States economy in 2024, with:
- GDP: $25.46 trillion 
- Population: 340 million
- Inflation Rate: 3.2%
- Unemployment: 3.8%
- Federal Funds Rate: 5.25%

## Agents

### The Federal Reserve
Role: Central bank of the United States
Location: Washington, D.C.
Key People:
- Chair Jerome Powell
- 7-member Board of Governors
- 12 regional Federal Reserve Bank presidents
Actions Available:
- Set federal funds rate target (range 0-10%)
- Conduct open market operations
- Set bank reserve requirements
Current Position:
- Primary concern is bringing inflation to 2% target
- Watching labor market strength
- Monitoring financial stability

### The Treasury Department
Role: Federal government's financial arm
Location: Washington, D.C.
Key People:
- Secretary Janet Yellen
Actions Available:
- Issue government bonds
- Collect taxes
- Implement fiscal policy
Current Position:
- Managing $34 trillion national debt
- Concerned about debt ceiling
- Monitoring tax revenues

### Major Commercial Banks (Top 5)
Names:
- JPMorgan Chase
- Bank of America
- Citigroup
- Wells Fargo
- Goldman Sachs
Actions Available:
- Set lending rates
- Issue loans
- Trade securities
Current Position:
- Strong capital ratios
- Cautious lending standards
- Growing digital banking focus

### Large Corporations (Fortune 100)
Examples:
- Apple
- Microsoft
- Amazon
- Walmart
- ExxonMobil
Actions Available:
- Set prices
- Hire/fire workers
- Make investments
Current Position:
- Strong profits
- Cautious about expansion
- Focus on AI/automation

### Small Businesses (Aggregate)
Representing:
- 33.2 million small businesses
- 61.7 million employees
Actions Available:
- Hire/fire workers
- Take loans
- Set prices
Current Position:
- Struggling with inflation
- Labor shortages
- Rising interest costs

### Consumer Groups (By Income)
Categories:
1. Top 1% (>$500k/year)
   - High saving rate
   - Investment focused
   - Price insensitive

2. Upper Middle (80-99th percentile)
   - Professional workers
   - Homeowners
   - Investment active

3. Middle Class (20-80th percentile)
   - Mix of owners/renters
   - Some savings
   - Price sensitive

4. Lower Income (<20th percentile)
   - Mostly renters
   - Limited savings
   - Highly price sensitive

## Interaction Rules

1. Interest Rate Changes
- Fed announces rate decision
- Banks adjust lending rates within 24 hours
- Businesses react within 1 week
- Consumers adjust spending within 1 month

2. Corporate Actions
- Quarterly earnings reports
- Monthly employment changes
- Weekly price adjustments

3. Consumer Behavior
- Daily spending decisions
- Monthly saving/investment choices
- Yearly wage negotiations

## Time Scale
- Each tick = 1 day
- Reports generated monthly
- Major decisions quarterly
- Full simulation runs 4 years
"""

URBAN_SIM = """# Urban Development Simulation - Seattle 2024

## Initial World State
Seattle, Washington:
- Population: 737,015
- Area: 217 km²
- Density: 3,396/km²
- Budget: $7.4 billion
- Housing Units: 368,000
- Median Home Price: $820,000
- Transit Ridership: 400,000 daily

## Agents

### City Government
1. Mayor Bruce Harrell
   Actions Available:
   - Propose budget changes
   - Issue executive orders
   - Appoint department heads
   Current Priorities:
   - Housing affordability
   - Public safety
   - Climate resilience

2. City Council (9 members)
   Actions Available:
   - Pass legislation
   - Approve/modify budget
   - Change zoning laws
   Districts: 7 geographic + 2 at-large
   Current Focus:
   - Housing density
   - Transit expansion
   - Police funding

### Development Entities

1. Major Developers (Top 5)
   - Vulcan Real Estate
   - Wright Runstad
   - Kilroy Realty
   - Urban Visions
   - Security Properties
   Actions Available:
   - Propose developments
   - Buy/sell property
   - Set rental rates
   Current Projects:
   - South Lake Union expansion
   - Denny Triangle towers
   - First Hill residential

2. Seattle Housing Authority
   Properties: 8,000 units
   Waitlist: 5,000 households
   Actions Available:
   - Build affordable housing
   - Manage public housing
   - Issue housing vouchers

### Transit Agencies

1. Sound Transit
   System:
   - Light Rail: 24 miles
   - Buses: 28 routes
   - Stations: 19
   Actions:
   - Adjust schedules
   - Plan expansions
   - Set fares

2. King County Metro
   Fleet: 1,540 buses
   Routes: 237
   Actions:
   - Route changes
   - Service frequency
   - Fleet management

### Population Groups

1. Tech Workers (25% of workforce)
   Characteristics:
   - Income: >$150k/year
   - Age: 25-40 majority
   - 70% renters
   Actions:
   - Housing choice
   - Commute mode
   - Spending patterns

2. Service Workers (30%)
   Characteristics:
   - Income: $30-50k/year
   - Age: 20-60 spread
   - 85% renters
   Actions:
   - Housing location
   - Transit usage
   - Work location

3. Families with Children (18%)
   Characteristics:
   - Mixed income levels
   - School priority
   - 60% homeowners
   Actions:
   - School choice
   - Housing type
   - Neighborhood selection

4. Retirees (15%)
   Characteristics:
   - Fixed incomes
   - Healthcare priority
   - 75% homeowners
   Actions:
   - Downsizing decisions
   - Service usage
   - Community engagement

### Business Districts

1. Downtown Core
   Stats:
   - 12 million sq ft office
   - 150,000 workers
   - 500 retail stores
   Actions:
   - Set lease rates
   - Building upgrades
   - Business mix

2. South Lake Union
   Stats:
   - Amazon HQ
   - 45,000 tech workers
   - 6 million sq ft office
   Actions:
   - Expansion plans
   - Amenity development
   - Transit integration

## Interaction Rules

1. Development Process
   - Proposal submission
   - 60-day public comment
   - Council review
   - Permit issuance
   Timeline: 6-18 months

2. Transit Changes
   - Quarterly service reviews
   - Annual major changes
   - 5-year planning cycles

3. Housing Market
   - Monthly price adjustments
   - Quarterly inventory updates
   - Yearly trend analysis

## Time Scale
- Each tick = 1 day
- Development cycles = quarters
- Major planning = yearly
- Simulation runs 10 years
"""

SIMULATIONS = {
    "organization": {
        "name": "Tech Company Simulation (Canva)",
        "description": "Simulates Canva's organizational structure and operations with specific roles and interactions",
        "content": ORGANIZATION_SIM
    },
    "economic": {
        "name": "US Economic Policy Simulation",
        "description": "Models US economy with Federal Reserve, Treasury, banks, businesses, and consumers",
        "content": ECONOMIC_SIM
    },
    "urban": {
        "name": "Seattle Urban Development",
        "description": "Simulates Seattle's urban development with government, developers, transit, and population groups",
        "content": URBAN_SIM
    }
}