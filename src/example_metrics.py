from .metrics import MetricDefinition

ORGANIZATION_METRICS = [
    MetricDefinition(
        name="employee_satisfaction",
        description="Average employee happiness score",
        type="numeric",
        initial_value=75,
        aggregation="average",
        target_value=85,
        target_direction="maximize"
    ),
    MetricDefinition(
        name="team_productivity",
        description="Overall team productivity index",
        type="percentage",
        initial_value=100,
        aggregation="latest",
        target_value=120,
        target_direction="maximize"
    ),
    MetricDefinition(
        name="project_completion_rate",
        description="Rate of project milestone completion",
        type="percentage",
        initial_value=0,
        aggregation="latest",
        target_value=90,
        target_direction="maximize"
    ),
    MetricDefinition(
        name="communication_effectiveness",
        description="Team communication effectiveness score",
        type="numeric",
        initial_value=70,
        aggregation="average",
        target_value=85,
        target_direction="maximize"
    )
]

URBAN_METRICS = [
    MetricDefinition(
        name="carbon_footprint",
        description="City carbon emissions (tons CO2)",
        type="numeric",
        initial_value=1000000,
        aggregation="latest",
        target_value=500000,
        target_direction="minimize"
    ),
    MetricDefinition(
        name="quality_of_life",
        description="Citizen quality of life index",
        type="numeric",
        initial_value=70,
        aggregation="average",
        target_value=85,
        target_direction="maximize"
    ),
    MetricDefinition(
        name="traffic_congestion",
        description="Average traffic congestion level",
        type="percentage",
        initial_value=45,
        aggregation="average",
        target_value=20,
        target_direction="minimize"
    ),
    MetricDefinition(
        name="green_space_coverage",
        description="Percentage of city area as green space",
        type="percentage",
        initial_value=15,
        aggregation="latest",
        target_value=30,
        target_direction="maximize"
    )
]

ECONOMIC_METRICS = [
    MetricDefinition(
        name="gdp_growth",
        description="GDP growth rate",
        type="percentage",
        initial_value=2.5,
        aggregation="latest",
        target_value=3.5,
        target_direction="maximize"
    ),
    MetricDefinition(
        name="inflation_rate",
        description="Annual inflation rate",
        type="percentage",
        initial_value=2.0,
        aggregation="latest",
        target_value=2.0,
        target_direction="target"
    ),
    MetricDefinition(
        name="unemployment_rate",
        description="Unemployment rate",
        type="percentage",
        initial_value=5.0,
        aggregation="latest",
        target_value=4.0,
        target_direction="minimize"
    ),
    MetricDefinition(
        name="income_inequality",
        description="Gini coefficient",
        type="numeric",
        initial_value=0.38,
        aggregation="latest",
        target_value=0.35,
        target_direction="minimize"
    )
]