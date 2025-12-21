# CHAPTER 5: IMPLEMENTATION AND DEPLOYMENT

## 5.3 Working of the Project

This chapter provides a comprehensive technical explanation of the AutoLight Analyser system, covering its procedural workflow, algorithmic approaches, and deployment architecture.

---

## 5.3.1 Procedural Workflow

### Overview

The AutoLight Analyser follows a systematic workflow that processes CAD files, analyzes lighting requirements, and generates intelligent fixture recommendations. The system operates through five primary phases:

1. **User Input and Authentication**
2. **CAD File Upload and Preprocessing**
3. **Lighting Analysis and Calculation**
4. **Fixture Recommendation Generation**
5. **Report Generation and Export**

### Detailed Step-by-Step Process

#### Phase 1: User Authentication and Session Management

The system begins when a user accesses the application. The authentication module verifies credentials and establishes a secure session. Upon successful login, the user is directed to the dashboard where project statistics and historical data are displayed.

**Process Flow:**
- User enters credentials (username/password)
- Django authentication middleware validates credentials
- Session token is generated and stored
- User role is verified (Admin/Architect/Vendor)
- Dashboard is populated with user-specific data

#### Phase 2: CAD File Upload and Processing

Once authenticated, users can upload CAD files (.dwg or .dxf format) containing architectural floor plans and lighting fixture placements.

**Upload Process:**
1. User selects project name and CAD file from local system
2. Optional symbol legend mapping can be provided (JSON format)
3. File is validated for format and size constraints
4. File is uploaded to secure media storage
5. CADFile database record is created with status 'pending'

**Processing Workflow:**
1. System updates CADFile status to 'processing'
2. ezdxf library parses the uploaded file
3. Block entities (INSERT) are extracted representing light fixtures
4. Closed polylines (LWPOLYLINE) are identified as room boundaries
5. Coordinate data and metadata are captured for each entity

**Extraction Details:**
- **Fixture Data**: Block name, X/Y/Z coordinates, rotation angle, layer
- **Room Data**: Boundary points, calculated area, layer information
- **Validation**: Area constraints (0.1 m² to 10,000 m²)

#### Phase 3: Lighting Requirement Calculation

The system employs advanced lighting engineering principles to calculate illumination requirements dynamically.

**Lux Calculation Algorithm:**

The required lux level is determined based on:
- Room type (bedroom, office, showroom, etc.)
- Room dimensions (length, width, height)
- Standard lighting codes and regulations

**Standard Lux Levels (IS 3646 and IES recommendations):**
- Bedroom: 150 lux
- Living Room: 200 lux
- Kitchen: 400 lux
- Office/Classroom: 500 lux
- Showroom: 750 lux
- Laboratory: 500 lux

**Required Lumens Formula:**

```
Required Lumens = (Room Area × Required Lux) / (Utilization Factor × Maintenance Factor)

Where:
- Room Area = Length × Width (in m²)
- Required Lux = Standard lux for room type
- Utilization Factor = 0.7 (accounts for light absorption and reflection)
- Maintenance Factor = 0.8 (accounts for lamp depreciation and dirt accumulation)
```

**Room Index Calculation:**

```
Room Index = (Length × Width) / (Height × (Length + Width))
```

This index helps determine the effectiveness of light distribution within the space.

#### Phase 4: Fixture Mapping and Recommendation

The system maps extracted CAD symbols to the lighting catalog database and generates intelligent recommendations.

**Mapping Process:**
1. Extract unique block names from CAD file
2. Match symbols with catalog entries using:
   - Exact symbol_name match
   - Fuzzy matching (first 3 characters)
   - User-provided legend mapping
3. Create Fixture records linking rooms to catalog items
4. Calculate quantities based on block count

**Recommendation Engine:**

The enhanced recommendation system provides three categories of alternatives:

**A. Below Budget Fixtures (₹ 0.7× to ₹ 1.0× current price)**
- Filters: 70-100% of current fixture cost
- Similar lumens output (±25%)
- Sorted by ascending cost
- Purpose: Cost-saving options

**B. Within Budget Fixtures (₹ 0.8× to ₹ 1.2× current price)**
- Filters: 80-120% of current fixture cost
- Similar lumens output (±25%)
- Sorted by lumens (descending), then cost
- Purpose: Comparable alternatives

**C. Above Budget Fixtures (₹ 1.0× to ₹ 1.3× current price)**
- Filters: 100-130% of current fixture cost
- Higher lumens output preferred
- Sorted by lumens (descending)
- Purpose: Premium upgrade options

**Efficiency Scoring:**

Each recommendation is assigned an efficiency score:

```
Luminous Efficacy = Lumens / Wattage (lm/W)
Cost Efficiency = Lumens / Unit Cost (lm/₹)
Efficiency Score = (Luminous Efficacy × 0.6) + (Cost Efficiency × 0.4)
```

Recommendations are sorted by efficiency score to prioritize value.

#### Phase 5: Analysis and Report Generation

The final phase involves calculating lighting adequacy and generating comprehensive reports.

**Current Lux Calculation:**

```
Total Lumens = Σ (Fixture Lumens × Quantity) for all fixtures in room
Effective Lumens = Total Lumens × Efficiency Factor (0.7)
Current Lux = Effective Lumens / Room Area
```

**Adequacy Check:**

```
Is Adequately Lit = (Current Lux ≥ Required Lux)
```

**Report Types:**

1. **PDF Report:**
   - Project information header
   - Room-by-room analysis tables
   - Fixture specifications and costs
   - Lighting adequacy status
   - Project summary with totals
   - Professional formatting with ReportLab

2. **CSV Report:**
   - Structured data export
   - Compatible with Excel/spreadsheets
   - Room details and fixture lists
   - Summary statistics
   - Easy data manipulation

3. **Interactive Dashboard:**
   - Real-time project statistics
   - Chart.js visualizations
   - Fixtures per room (bar chart)
   - Fixture type distribution (pie chart)
   - Lux trends across projects (line chart)

### Workflow Diagram Description

**[Workflow Flowchart - To be created in Draw.io or Lucidchart]**

```
Start
  ↓
[User Login/Authentication]
  ↓
[Dashboard - View Projects]
  ↓
[Upload CAD File] → [Enter Project Name + Optional Legend]
  ↓
[File Validation] → [Check Format (.dwg/.dxf)]
  ↓
[Parse CAD File] → [Extract Blocks + Polylines]
  ↓
[Identify Rooms] → [Calculate Areas]
  ↓
[Map Symbols to Catalog] → [Create Fixture Records]
  ↓
[Calculate Lux Requirements] → [Based on Room Type + Dimensions]
  ↓
[Calculate Current Lux] → [Sum Fixture Lumens]
  ↓
[Generate Recommendations] → [Budget-based Filtering]
  ↓
[Display Results] → [Interactive UI with Alternatives]
  ↓
[User Selects Fixtures] → [Update if needed]
  ↓
[Generate Report] → [PDF/CSV]
  ↓
[Download/View Report]
  ↓
End
```

### Data Flow

**Input Data:**
- CAD files (.dwg/.dxf) containing architectural plans
- User credentials and project metadata
- Optional symbol legend (JSON)
- Room type selections

**Processing Data:**
- Parsed block entities with coordinates
- Extracted polyline boundaries
- Calculated room dimensions and areas
- Matched fixture catalog entries
- Computed lux levels

**Output Data:**
- Lighting analysis results (current vs required lux)
- Fixture recommendations categorized by budget
- Cost calculations with INR currency
- Professional PDF and CSV reports
- Dashboard analytics and visualizations

### System State Transitions

The CADFile model transitions through distinct states:

1. **Pending** → Initial upload state
2. **Processing** → Active parsing and analysis
3. **Completed** → Successful processing, results available
4. **Failed** → Error encountered, error_message populated

Each state transition is logged with timestamps for audit trails.

### Error Handling and Validation

The system implements robust error handling:

- **File Format Validation**: Only .dwg and .dxf files accepted
- **Area Constraints**: Rooms must be between 0.1 m² and 10,000 m²
- **Symbol Mapping Failures**: Unmapped symbols are logged and skipped
- **Calculation Safeguards**: Division by zero checks, null value handling
- **User Feedback**: Clear error messages displayed in UI
- **Transaction Rollback**: Database consistency maintained on errors

---

## 5.3.2 Algorithmic Approaches Used

This section details the key algorithms implemented in the AutoLight Analyser system, providing mathematical foundations, pseudocode, and complexity analysis.

### Algorithm 1: Dynamic Lux Requirement Calculator

**Purpose**: Calculate the required illuminance (lux) for a room based on its type, dimensions, and standard lighting regulations.

**Inputs**:
- room_type: String (e.g., "office", "bedroom", "showroom")
- room_area: Float (in m²)
- room_length: Float (in m, optional)
- room_width: Float (in m, optional)
- room_height: Float (in m, default 3.0)

**Outputs**:
- required_lux: Float (recommended illuminance in lux)
- required_lumens: Float (total lumens needed)

**Mathematical Basis**:

The algorithm is based on the lumen method from the Illuminating Engineering Society (IES):

```
Required Lumens = (A × E) / (CU × MF)

Where:
A  = Room Area (m²)
E  = Required Illuminance (lux)
CU = Coefficient of Utilization (0.7)
MF = Maintenance Factor (0.8)
```

**Pseudocode**:

```
ALGORITHM DynamicLuxCalculator

INPUT: room_type, room_area, room_length, room_width, room_height

BEGIN
    // Define standard lux levels based on IS 3646 and IES guidelines
    LUX_STANDARDS = {
        "bedroom": 150,
        "living_room": 200,
        "kitchen": 400,
        "bathroom": 200,
        "office": 500,
        "classroom": 500,
        "conference_room": 300,
        "hallway": 150,
        "showroom": 750,
        "warehouse": 200,
        "laboratory": 500,
        "hospital_room": 300,
        "other": 300
    }
    
    // Step 1: Determine required lux from room type
    IF room_type IN LUX_STANDARDS THEN
        required_lux ← LUX_STANDARDS[room_type]
    ELSE
        required_lux ← 300  // Default value
    END IF
    
    // Step 2: Calculate room index for utilization factor adjustment
    IF room_length AND room_width ARE PROVIDED THEN
        room_index ← (room_length × room_width) / 
                     (room_height × (room_length + room_width))
    ELSE
        room_index ← 1.0  // Default
    END IF
    
    // Step 3: Define efficiency factors
    utilization_factor ← 0.7   // Light absorption and reflection
    maintenance_factor ← 0.8   // Lamp depreciation and dirt
    
    // Step 4: Calculate required lumens
    basic_lumens ← room_area × required_lux
    required_lumens ← basic_lumens / (utilization_factor × maintenance_factor)
    required_lumens ← CEILING(required_lumens)  // Round up
    
    // Step 5: Return results
    RETURN (required_lux, required_lumens)
END
```

**Time Complexity**: O(1) - Constant time lookup and arithmetic operations

**Space Complexity**: O(1) - Fixed-size data structures

**Example Execution**:

```
Input:
  room_type = "office"
  room_area = 50 m²
  room_height = 3.0 m

Processing:
  required_lux = 500 lux (from LUX_STANDARDS["office"])
  basic_lumens = 50 × 500 = 25,000 lumens
  required_lumens = 25,000 / (0.7 × 0.8) = 44,643 lumens

Output:
  required_lux = 500 lux
  required_lumens = 44,643 lumens
```

---

### Algorithm 2: Budget-Based Recommendation Engine

**Purpose**: Generate fixture recommendations categorized by budget ranges (below, within, above current price) while maintaining similar lighting specifications.

**Inputs**:
- current_fixture_cost: Decimal (in ₹)
- catalog_item: LightingCatalog object
- budget_range: String ("below", "within", "above", "all")
- limit: Integer (maximum recommendations)

**Outputs**:
- recommendations: List of LightingCatalog objects sorted by relevance

**Pseudocode**:

```
ALGORITHM BudgetBasedRecommendationEngine

INPUT: current_fixture_cost, catalog_item, budget_range, limit

BEGIN
    // Step 1: Calculate budget thresholds
    below_threshold ← current_fixture_cost × 0.8
    above_threshold ← current_fixture_cost × 1.2
    
    // Step 2: Calculate lumens range for quality maintenance
    min_lumens ← catalog_item.lumens × 0.75
    max_lumens ← catalog_item.lumens × 1.25
    
    // Step 3: Base query - similar specifications
    base_query ← SELECT * FROM LightingCatalog
                 WHERE lumens >= min_lumens
                   AND lumens <= max_lumens
                   AND id != catalog_item.id
    
    recommendations ← EMPTY_LIST
    
    // Step 4: Below budget recommendations
    IF budget_range == "below" OR budget_range == "all" THEN
        below_budget ← SELECT * FROM base_query
                       WHERE unit_cost < current_fixture_cost
                         AND unit_cost >= current_fixture_cost × 0.7
                       ORDER BY unit_cost ASC
                       LIMIT (limit / 3)
        
        recommendations ← recommendations + below_budget
    END IF
    
    // Step 5: Within budget recommendations
    IF budget_range == "within" OR budget_range == "all" THEN
        within_budget ← SELECT * FROM base_query
                        WHERE unit_cost >= below_threshold
                          AND unit_cost <= above_threshold
                        ORDER BY lumens DESC, unit_cost ASC
                        LIMIT (limit / 3)
        
        recommendations ← recommendations + within_budget
    END IF
    
    // Step 6: Above budget recommendations
    IF budget_range == "above" OR budget_range == "all" THEN
        above_budget ← SELECT * FROM base_query
                       WHERE unit_cost > current_fixture_cost
                         AND unit_cost <= current_fixture_cost × 1.3
                       ORDER BY lumens DESC, unit_cost ASC
                       LIMIT (limit / 3)
        
        recommendations ← recommendations + above_budget
    END IF
    
    // Step 7: Remove duplicates while preserving order
    seen ← EMPTY_SET
    unique_recommendations ← EMPTY_LIST
    
    FOR each item IN recommendations DO
        IF item.id NOT IN seen THEN
            ADD item.id TO seen
            ADD item TO unique_recommendations
        END IF
    END FOR
    
    // Step 8: Calculate efficiency scores
    FOR each item IN unique_recommendations DO
        item.efficiency_score ← CalculateEfficiencyScore(item)
    END FOR
    
    // Step 9: Sort by efficiency score (descending)
    SORT unique_recommendations BY efficiency_score DESC
    
    // Step 10: Limit results
    unique_recommendations ← unique_recommendations[0:limit]
    
    RETURN unique_recommendations
END

FUNCTION CalculateEfficiencyScore(fixture_catalog)
BEGIN
    IF fixture_catalog.wattage <= 0 OR fixture_catalog.unit_cost <= 0 THEN
        RETURN 0.0
    END IF
    
    // Luminous efficacy (energy efficiency)
    luminous_efficacy ← fixture_catalog.lumens / fixture_catalog.wattage
    
    // Cost efficiency (value for money)
    cost_efficiency ← fixture_catalog.lumens / fixture_catalog.unit_cost
    
    // Weighted combined score
    efficiency_score ← (luminous_efficacy × 0.6) + (cost_efficiency × 0.4)
    
    RETURN ROUND(efficiency_score, 2)
END
```

**Time Complexity**: O(n log n) where n is the number of matching fixtures
- Database queries: O(n)
- Sorting by efficiency: O(n log n)
- Duplicate removal: O(n)

**Space Complexity**: O(n) for storing recommendations

**Example Execution**:

```
Input:
  current_fixture_cost = ₹2,500
  catalog_item.lumens = 3,000
  budget_range = "all"
  limit = 10

Processing:
  below_threshold = ₹2,000
  above_threshold = ₹3,000
  min_lumens = 2,250
  max_lumens = 3,750
  
  Below Budget Query:
    cost: ₹1,750 to ₹2,500
    Found: 3 fixtures
  
  Within Budget Query:
    cost: ₹2,000 to ₹3,000
    Found: 4 fixtures
  
  Above Budget Query:
    cost: ₹2,500 to ₹3,250
    Found: 3 fixtures
  
  Total: 10 fixtures
  After deduplication: 9 unique fixtures
  After efficiency scoring and sorting: 9 fixtures ordered by value

Output:
  List of 9 LightingCatalog objects with efficiency scores
```

---

### Algorithm 3: Room Area Calculator (Shoelace Formula)

**Purpose**: Calculate the area of a room from its boundary coordinates extracted from CAD polylines.

**Inputs**:
- points: List of (x, y) coordinate tuples representing room boundary

**Outputs**:
- area: Float (room area in m²)

**Mathematical Basis**:

The Shoelace formula (Gauss's area formula) for polygon area:

```
Area = 0.5 × |Σ(x_i × y_{i+1} - x_{i+1} × y_i)|

Where:
- (x_i, y_i) are consecutive vertices
- Summation from i=0 to n-1
- (x_n, y_n) = (x_0, y_0) (closed polygon)
```

**Pseudocode**:

```
ALGORITHM RoomAreaCalculator

INPUT: points  // List of (x, y) tuples

BEGIN
    // Step 1: Validate input
    IF LENGTH(points) < 3 THEN
        RETURN 0.0  // Not a valid polygon
    END IF
    
    // Step 2: Apply Shoelace formula
    area ← 0.0
    n ← LENGTH(points)
    
    FOR i ← 0 TO n-1 DO
        j ← (i + 1) MOD n  // Next vertex (wrap around)
        area ← area + (points[i].x × points[j].y)
        area ← area - (points[j].x × points[i].y)
    END FOR
    
    // Step 3: Calculate absolute value and divide by 2
    raw_area ← ABS(area) / 2.0
    
    // Step 4: Unit conversion (assume CAD units in millimeters)
    area_m2 ← raw_area / 1,000,000.0  // mm² to m²
    
    // Step 5: Handle alternative unit systems
    IF area_m2 > 10,000 THEN
        // Likely in cm² or other units
        area_m2 ← raw_area / 10,000.0
    ELSE IF area_m2 < 0.1 THEN
        // Already in meters
        area_m2 ← raw_area
    END IF
    
    // Step 6: Validate result
    IF area_m2 < 0.1 THEN
        area_m2 ← 1.0  // Minimum valid room size
    ELSE IF area_m2 > 10,000 THEN
        RETURN ERROR  // Likely parsing error
    END IF
    
    RETURN ROUND(area_m2, 2)
END
```

**Time Complexity**: O(n) where n is the number of vertices

**Space Complexity**: O(1) - only storing cumulative sum

**Example Execution**:

```
Input:
  points = [(0, 0), (5000, 0), (5000, 4000), (0, 4000)]  // mm
  // Rectangle: 5m × 4m

Processing:
  Shoelace calculation:
    (0 × 0) - (5000 × 0) = 0
    (5000 × 4000) - (5000 × 0) = 20,000,000
    (5000 × 4000) - (0 × 4000) = 20,000,000
    (0 × 0) - (0 × 4000) = 0
    Sum = 40,000,000
  
  raw_area = |40,000,000| / 2 = 20,000,000 mm²
  area_m2 = 20,000,000 / 1,000,000 = 20 m²

Output:
  area = 20.0 m²
```

---

### Algorithm 4: CAD Symbol Mapper

**Purpose**: Map extracted CAD block symbols to lighting fixture catalog entries using exact matching, fuzzy matching, and user-provided legends.

**Inputs**:
- symbols: List of unique block names from CAD
- legend: Optional dictionary mapping CAD symbols to catalog symbol_names
- catalog_database: LightingCatalog table

**Outputs**:
- mapping: Dictionary {symbol: LightingCatalog object or None}

**Pseudocode**:

```
ALGORITHM CADSymbolMapper

INPUT: symbols, legend, catalog_database

BEGIN
    mapping ← EMPTY_DICTIONARY
    
    FOR each symbol IN symbols DO
        // Step 1: Apply legend translation if provided
        IF legend IS PROVIDED AND symbol IN legend THEN
            catalog_name ← legend[symbol]
        ELSE
            catalog_name ← symbol
        END IF
        
        // Step 2: Try exact match
        catalog_item ← SELECT * FROM catalog_database
                       WHERE symbol_name == catalog_name
        
        IF catalog_item IS FOUND THEN
            mapping[symbol] ← catalog_item
            CONTINUE  // Move to next symbol
        END IF
        
        // Step 3: Try fuzzy match (first 3 characters)
        IF LENGTH(symbol) >= 3 THEN
            prefix ← symbol[0:3]
            similar_items ← SELECT * FROM catalog_database
                            WHERE symbol_name CONTAINS prefix
                            ORDER BY symbol_name
                            LIMIT 1
            
            IF similar_items IS NOT EMPTY THEN
                mapping[symbol] ← similar_items[0]
                CONTINUE
            END IF
        END IF
        
        // Step 4: No match found
        mapping[symbol] ← NULL
        LOG_WARNING("Unmapped symbol: " + symbol)
    END FOR
    
    RETURN mapping
END
```

**Time Complexity**: O(s × log c) where s = number of symbols, c = catalog size
- Exact match: O(log c) per symbol (indexed lookup)
- Fuzzy match: O(c) per symbol (pattern matching)

**Space Complexity**: O(s) for storing mapping dictionary

---

### Algorithm 5: Current Lux Calculator

**Purpose**: Calculate the actual illuminance level in a room based on installed fixtures.

**Inputs**:
- fixtures_list: List of Fixture objects in the room
- room_area: Float (in m²)

**Outputs**:
- current_lux: Float (measured illuminance in lux)

**Pseudocode**:

```
ALGORITHM CurrentLuxCalculator

INPUT: fixtures_list, room_area

BEGIN
    // Step 1: Validate room area
    IF room_area <= 0 THEN
        RETURN 0.0
    END IF
    
    // Step 2: Calculate total lumens from all fixtures
    total_lumens ← 0
    
    FOR each fixture IN fixtures_list DO
        fixture_lumens ← fixture.catalog_item.lumens × fixture.quantity
        total_lumens ← total_lumens + fixture_lumens
    END FOR
    
    // Step 3: Check if any fixtures exist
    IF total_lumens == 0 THEN
        RETURN 0.0
    END IF
    
    // Step 4: Apply lighting efficiency factor
    efficiency_factor ← 0.7  // Accounts for:
                             // - Light absorption by surfaces
                             // - Reflection losses
                             // - Non-uniform distribution
    
    effective_lumens ← total_lumens × efficiency_factor
    
    // Step 5: Calculate lux (lumens per square meter)
    current_lux ← effective_lumens / room_area
    
    // Step 6: Round to 2 decimal places
    current_lux ← ROUND(current_lux, 2)
    
    RETURN current_lux
END
```

**Time Complexity**: O(f) where f is the number of fixtures in the room

**Space Complexity**: O(1) - only storing cumulative sum

---

### Algorithm 6: Fixture Requirement Calculator

**Purpose**: Determine the optimal number of fixtures needed to achieve target illuminance.

**Inputs**:
- room_area: Float (in m²)
- lumens_per_fixture: Integer (lumens output per fixture)
- required_lux: Float (target illuminance)

**Outputs**:
- fixtures_needed: Integer (rounded up to ensure adequate lighting)

**Pseudocode**:

```
ALGORITHM FixtureRequirementCalculator

INPUT: room_area, lumens_per_fixture, required_lux

BEGIN
    // Step 1: Validate inputs
    IF lumens_per_fixture <= 0 THEN
        RETURN 0
    END IF
    
    // Step 2: Calculate total lumens required
    total_lumens_required ← room_area × required_lux
    
    // Step 3: Apply efficiency factor
    efficiency_factor ← 0.7
    effective_lumens_per_fixture ← lumens_per_fixture × efficiency_factor
    
    // Step 4: Calculate number of fixtures
    fixtures_needed ← total_lumens_required / effective_lumens_per_fixture
    
    // Step 5: Round up to ensure adequate lighting
    fixtures_needed ← CEILING(fixtures_needed)
    
    RETURN fixtures_needed
END
```

**Time Complexity**: O(1) - simple arithmetic operations

**Space Complexity**: O(1)

---

### Summary of Algorithmic Complexity

| Algorithm | Time Complexity | Space Complexity | Primary Operation |
|-----------|----------------|------------------|-------------------|
| Lux Calculator | O(1) | O(1) | Lookup + Arithmetic |
| Recommendation Engine | O(n log n) | O(n) | Database Query + Sort |
| Room Area Calculator | O(n) | O(1) | Polygon Area Calculation |
| Symbol Mapper | O(s × log c) | O(s) | Database Matching |
| Current Lux Calculator | O(f) | O(1) | Summation |
| Fixture Calculator | O(1) | O(1) | Arithmetic |

**Overall System Complexity**: O(n log n) dominated by the recommendation engine sorting operation.

---

## 5.3.3 Project Deployment

This section describes the deployment architecture, component structure, and system infrastructure of the AutoLight Analyser.

### System Architecture Overview

The AutoLight Analyser employs a three-tier architecture pattern:

1. **Presentation Tier** - Frontend user interface
2. **Application Tier** - Backend business logic and API
3. **Data Tier** - Database and file storage

### Component Architecture

#### Frontend Components

**Technology Stack**:
- React 18.x (UI framework)
- TypeScript (type-safe JavaScript)
- Tailwind CSS (utility-first styling)
- Chart.js (data visualization)
- html2pdf.js (client-side PDF generation)
- Vite (build tool and dev server)

**Key Components**:

1. **Dashboard Component** (`Dashboard.tsx`)
   - Displays project statistics
   - Renders interactive charts
   - Shows recent project history
   - Implements real-time data updates

2. **Upload Component** (`Upload.tsx`)
   - File input with drag-and-drop
   - Form validation
   - Progress indicators
   - Legend mapping interface

3. **Results Component** (`Results.tsx`)
   - Room-by-room analysis display
   - Fixture recommendations interface
   - Interactive price calculator
   - Alternative fixture selector

4. **Layout Component** (`Layout.tsx`)
   - Navigation bar
   - User authentication status
   - Responsive sidebar
   - Theme toggle (dark/light mode)

**Component Diagram Description**:

```
[User Browser]
    ↓
[React Application]
    ├─ [Layout Component]
    │   ├─ [Navigation Bar]
    │   ├─ [Sidebar Menu]
    │   └─ [Theme Switcher]
    │
    ├─ [Dashboard Component]
    │   ├─ [Statistics Cards]
    │   ├─ [Chart.js Visualizations]
    │   │   ├─ [Bar Chart - Fixtures per Room]
    │   │   ├─ [Pie Chart - Fixture Types]
    │   │   └─ [Line Chart - Lux Trends]
    │   └─ [Recent Projects Table]
    │
    ├─ [Upload Component]
    │   ├─ [File Input (Drag & Drop)]
    │   ├─ [Project Name Input]
    │   ├─ [Legend Mapper (Optional)]
    │   └─ [Submit Button]
    │
    ├─ [Results Component]
    │   ├─ [Room Information Panel]
    │   ├─ [Fixtures Table]
    │   ├─ [Recommendations Section]
    │   │   ├─ [Below Budget]
    │   │   ├─ [Within Budget]
    │   │   └─ [Above Budget]
    │   ├─ [Cost Calculator]
    │   └─ [Report Export Buttons]
    │
    └─ [Profile Component]
        ├─ [User Information]
        └─ [Settings]
```

#### Backend Components

**Technology Stack**:
- Django 6.0 (web framework)
- Python 3.12+ (programming language)
- ezdxf (CAD file parsing)
- ReportLab (PDF generation)
- Celery (async task processing)
- Redis (task queue broker)

**Key Modules**:

1. **Models Layer** (`models.py`)
   - LightingCatalog: Fixture database
   - CADFile: Uploaded file tracking
   - Room: Detected space with dimensions
   - Fixture: Installed lighting units
   - Report: Generated documents

2. **Views Layer** (`views.py`)
   - dashboard: Project overview
   - upload_cad: File handling
   - results: Analysis display
   - generate_report: PDF/CSV creation
   - update_fixture_selection: AJAX API

3. **Utils Layer** (`utils.py`)
   - parse_cad: CAD file parser
   - calculate_required_fixtures: Lighting math
   - generate_pdf_report: ReportLab integration
   - get_budget_based_recommendations: Recommendation engine
   - calculate_fixture_efficiency_score: Scoring algorithm

4. **Forms Layer** (`forms.py`)
   - CADUploadForm: File upload validation
   - UserRegistrationForm: Account creation

**Django Component Diagram**:

```
[Django Application Server]
    │
    ├─ [URL Dispatcher]
    │   └─ routing configuration (urls.py)
    │
    ├─ [Middleware Stack]
    │   ├─ Authentication Middleware
    │   ├─ CSRF Protection
    │   ├─ Session Management
    │   └─ CORS Headers
    │
    ├─ [Views Layer]
    │   ├─ Function-Based Views
    │   │   ├─ dashboard()
    │   │   ├─ upload_cad()
    │   │   ├─ results()
    │   │   └─ generate_report()
    │   └─ API Endpoints (AJAX)
    │       └─ update_fixture_selection()
    │
    ├─ [Business Logic (Utils)]
    │   ├─ CAD Parser (ezdxf)
    │   ├─ Lighting Calculators
    │   ├─ Recommendation Engine
    │   └─ Report Generators
    │
    ├─ [Models Layer (ORM)]
    │   ├─ LightingCatalog
    │   ├─ CADFile
    │   ├─ Room
    │   ├─ Fixture
    │   └─ Report
    │
    ├─ [Forms Layer]
    │   ├─ Validation Logic
    │   └─ Data Cleaning
    │
    └─ [Admin Interface]
        └─ Django Admin Panel
```

### Database Schema

**Technology**: SQLite3 (development), PostgreSQL (production-ready)

**Entity-Relationship Diagram Description**:

```
[User]
  ├─ id (PK)
  ├─ username
  ├─ email
  ├─ password (hashed)
  └─ groups (FK to Groups)
       │
       └── has many ──► [CADFile]
                         ├─ id (PK)
                         ├─ user_id (FK)
                         ├─ project_name
                         ├─ filename
                         ├─ file (FileField)
                         ├─ status (pending/processing/completed/failed)
                         ├─ uploaded_at
                         └─ processed_at
                              │
                              ├── has many ──► [Room]
                              │                 ├─ id (PK)
                              │                 ├─ cad_file_id (FK)
                              │                 ├─ name
                              │                 ├─ room_type
                              │                 ├─ length (nullable)
                              │                 ├─ width (nullable)
                              │                 ├─ area
                              │                 ├─ height
                              │                 └─ required_lux
                              │                      │
                              │                      └── has many ──► [Fixture]
                              │                                        ├─ id (PK)
                              │                                        ├─ room_id (FK)
                              │                                        ├─ lighting_catalog_id (FK)
                              │                                        ├─ quantity
                              │                                        ├─ x_coordinate
                              │                                        └─ y_coordinate
                              │
                              └── has many ──► [Report]
                                                ├─ id (PK)
                                                ├─ cad_file_id (FK)
                                                ├─ report_type (pdf/csv)
                                                ├─ file_path
                                                └─ generated_at

[LightingCatalog] (Referenced by Fixture)
  ├─ id (PK)
  ├─ symbol_name (unique)
  ├─ model_number
  ├─ brand
  ├─ lumens
  ├─ wattage
  ├─ beam_angle
  ├─ color_temp
  ├─ unit_cost (INR)
  ├─ image (optional)
  ├─ created_at
  └─ updated_at
```

### Deployment Diagram

**Infrastructure Components**:

```
[Client Tier]
    ├─ Web Browsers (Chrome, Firefox, Safari, Edge)
    ├─ Mobile Browsers
    └─ Desktop Applications (future)
         │
         │ HTTPS (Port 443)
         ↓
[Load Balancer / Reverse Proxy]
    └─ Nginx / Apache
         │
         ├─ Static Files Serving
         │   ├─ CSS
         │   ├─ JavaScript bundles
         │   └─ Images
         │
         └─ Proxy to Application Server
              │
              ↓
[Application Server Tier]
    ├─ Django Application Server
    │   ├─ Gunicorn / uWSGI (WSGI server)
    │   ├─ Django Framework
    │   ├─ Business Logic
    │   └─ API Endpoints
    │
    ├─ Task Queue (Celery Workers)
    │   ├─ CAD Processing Tasks
    │   ├─ Report Generation Tasks
    │   └─ Email Notifications
    │
    └─ Task Broker (Redis)
        └─ Message Queue
              │
              ↓
[Data Tier]
    ├─ Database Server
    │   ├─ PostgreSQL (production)
    │   ├─ SQLite3 (development)
    │   └─ Connection Pool
    │
    └─ File Storage
        ├─ Media Files
        │   ├─ CAD Files (/media/cad_files/)
        │   ├─ Fixture Images (/media/fixtures/)
        │   └─ Generated Reports (/media/reports/)
        │
        └─ Static Files (compiled assets)
            ├─ CSS bundles
            ├─ JavaScript bundles
            └─ Font files
```

### Deployment Process

#### Development Environment

**Setup Steps**:

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd autolight_project
   ```

2. **Install Dependencies**:
   ```bash
   # Python dependencies
   pip install -r requirements.txt
   
   # Node dependencies
   npm install
   ```

3. **Database Setup**:
   ```bash
   python manage.py migrate
   python manage.py load_sample_data
   python manage.py createsuperuser
   ```

4. **Start Development Servers**:
   ```bash
   # Terminal 1: Django backend
   python manage.py runserver 0.0.0.0:8000
   
   # Terminal 2: React frontend (if separate)
   npm run dev
   ```

5. **Access Application**:
   - Backend: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

#### Production Deployment

**Technology Stack**:
- **Web Server**: Nginx (reverse proxy and static file serving)
- **WSGI Server**: Gunicorn (Python application server)
- **Process Manager**: Supervisor or systemd
- **Database**: PostgreSQL 14+
- **Cache**: Redis 6+
- **Operating System**: Ubuntu 22.04 LTS or similar

**Deployment Steps**:

1. **Server Preparation**:
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install python3.12 python3-pip postgresql redis-server nginx
   ```

2. **Application Setup**:
   ```bash
   # Create application user
   sudo useradd -m -d /opt/autolight autolight
   
   # Clone and setup
   cd /opt/autolight
   git clone <repository-url> app
   cd app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Database Configuration**:
   ```bash
   # Create PostgreSQL database
   sudo -u postgres createdb autolight_db
   sudo -u postgres createuser autolight_user
   
   # Grant permissions
   sudo -u postgres psql
   ALTER USER autolight_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE autolight_db TO autolight_user;
   ```

4. **Django Configuration**:
   ```python
   # settings.py (production)
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'autolight_db',
           'USER': 'autolight_user',
           'PASSWORD': 'secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   
   # Static files
   STATIC_ROOT = '/opt/autolight/static/'
   MEDIA_ROOT = '/opt/autolight/media/'
   ```

5. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

6. **Gunicorn Configuration**:
   ```bash
   # /opt/autolight/gunicorn_config.py
   bind = "127.0.0.1:8000"
   workers = 4
   worker_class = "sync"
   timeout = 120
   accesslog = "/var/log/gunicorn/access.log"
   errorlog = "/var/log/gunicorn/error.log"
   ```

7. **Nginx Configuration**:
   ```nginx
   # /etc/nginx/sites-available/autolight
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       location /static/ {
           alias /opt/autolight/static/;
       }
       
       location /media/ {
           alias /opt/autolight/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

8. **Systemd Service**:
   ```ini
   # /etc/systemd/system/autolight.service
   [Unit]
   Description=AutoLight Gunicorn Daemon
   After=network.target
   
   [Service]
   User=autolight
   Group=www-data
   WorkingDirectory=/opt/autolight/app
   Environment="PATH=/opt/autolight/app/venv/bin"
   ExecStart=/opt/autolight/app/venv/bin/gunicorn \
             --config /opt/autolight/gunicorn_config.py \
             autolight_project.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```

9. **Celery Configuration** (for async tasks):
   ```ini
   # /etc/systemd/system/celery-worker.service
   [Unit]
   Description=Celery Worker
   After=network.target
   
   [Service]
   Type=forking
   User=autolight
   Group=www-data
   WorkingDirectory=/opt/autolight/app
   Environment="PATH=/opt/autolight/app/venv/bin"
   ExecStart=/opt/autolight/app/venv/bin/celery -A autolight_project worker \
             --loglevel=info --concurrency=4
   
   [Install]
   WantedBy=multi-user.target
   ```

10. **Start Services**:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable autolight celery-worker nginx redis
    sudo systemctl start autolight celery-worker nginx redis
    ```

11. **SSL Certificate (Let's Encrypt)**:
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

### Security Considerations

1. **Authentication & Authorization**:
   - Django's built-in authentication system
   - Role-based access control (Admin, Architect, Vendor)
   - Session management with secure cookies
   - CSRF protection enabled

2. **Data Security**:
   - Password hashing (PBKDF2 algorithm)
   - SQL injection prevention (ORM parameterized queries)
   - XSS protection (template auto-escaping)
   - File upload validation (type and size checks)

3. **Network Security**:
   - HTTPS enforced in production
   - HSTS headers enabled
   - Firewall configuration (UFW)
   - Rate limiting on sensitive endpoints

4. **File Security**:
   - Uploaded files stored outside web root
   - Generated reports have unique names
   - Media files served through Django (permission checks)

### Monitoring and Logging

**Log Files**:
- Application logs: `/var/log/autolight/app.log`
- Gunicorn access: `/var/log/gunicorn/access.log`
- Gunicorn errors: `/var/log/gunicorn/error.log`
- Nginx access: `/var/log/nginx/access.log`
- Nginx errors: `/var/log/nginx/error.log`
- Celery logs: `/var/log/celery/worker.log`

**Monitoring Tools** (Optional):
- **Sentry**: Error tracking and performance monitoring
- **New Relic**: Application performance monitoring (APM)
- **Prometheus + Grafana**: Metrics collection and visualization
- **Django Debug Toolbar**: Development debugging

### Backup Strategy

1. **Database Backups**:
   ```bash
   # Daily cron job
   0 2 * * * pg_dump autolight_db | gzip > /backup/autolight_db_$(date +\%Y\%m\%d).sql.gz
   ```

2. **Media File Backups**:
   ```bash
   # Weekly rsync
   0 3 * * 0 rsync -az /opt/autolight/media/ /backup/media/
   ```

3. **Code Backups**:
   - Git repository (hosted on GitHub/GitLab)
   - Tagged releases for version control

### Scalability Considerations

**Horizontal Scaling**:
- Multiple Gunicorn workers (CPU-bound tasks)
- Multiple Celery workers (I/O-bound tasks)
- Load balancer distribution (Nginx upstream)
- Database connection pooling (pgBouncer)

**Vertical Scaling**:
- Increase server resources (CPU, RAM)
- Optimize database queries (indexes, query optimization)
- Caching frequently accessed data (Redis)
- CDN for static file delivery

**Performance Optimization**:
- Database query optimization (select_related, prefetch_related)
- Static file compression (gzip, Brotli)
- Image optimization and lazy loading
- Asynchronous task processing (Celery)
- Browser caching headers
- Database indexing on frequently queried fields

---

## Summary

This chapter has provided a comprehensive technical overview of the AutoLight Analyser system, covering:

1. **Procedural Workflow**: Detailed explanation of the user journey from authentication through report generation, including all intermediate processing steps.

2. **Algorithmic Approaches**: Six core algorithms with mathematical foundations, pseudocode, complexity analysis, and practical examples.

3. **Deployment Architecture**: Complete infrastructure setup from development to production, including component diagrams, database schema, and deployment processes.

The system demonstrates modern software engineering principles with scalable architecture, efficient algorithms, and robust deployment strategies suitable for real-world applications in architectural lighting design.

---

## References

1. Illuminating Engineering Society (IES) Lighting Handbook
2. IS 3646: Indian Standard Code of Practice for Interior Illumination
3. Django 6.0 Official Documentation
4. ezdxf Documentation - CAD File Processing Library
5. ReportLab User Guide - PDF Generation
6. PostgreSQL Performance Tuning Guide
7. Nginx Configuration Best Practices
8. Celery Distributed Task Queue Documentation
9. Chart.js Data Visualization Library
10. React 18 Official Documentation

---

**Document Prepared For**: Final Year Engineering Project
**Project Title**: AutoLight Analyser - Intelligent Lighting Recommendation System
**Academic Institution**: [Your University Name]
**Department**: Computer Science and Engineering / Electronics and Communication Engineering
**Date**: December 2024

---
