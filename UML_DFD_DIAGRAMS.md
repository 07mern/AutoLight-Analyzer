# AutoLight Analyser - UML and DFD Diagrams

This document provides detailed textual descriptions of all UML and Data Flow Diagrams for the AutoLight Analyser project. These descriptions can be used to recreate the diagrams in tools like Draw.io, Lucidchart, StarUML, or PlantUML.

---

## 1. USE CASE DIAGRAM

### Description
The Use Case Diagram illustrates the interactions between different actors (users) and the AutoLight Analyser system.

### Actors

1. **Guest User** (Unauthenticated)
2. **Architect** (Registered User)
3. **Administrator** (System Admin)
4. **Vendor** (Catalog Manager)

### Use Cases

#### Guest User Use Cases:
- **Register Account**
  - Description: Create a new user account
  - Pre-condition: None
  - Post-condition: User account created, logged in

- **Login**
  - Description: Authenticate using credentials
  - Pre-condition: User must be registered
  - Post-condition: Session established

#### Architect Use Cases:
- **View Dashboard**
  - Description: See project statistics and charts
  - Pre-condition: Must be logged in
  - Post-condition: Dashboard data displayed

- **Upload CAD File**
  - Description: Upload .dwg or .dxf file with project details
  - Pre-condition: Must be logged in
  - Post-condition: CAD file uploaded and queued for processing
  - Extends: Provide Symbol Legend (optional)

- **View Analysis Results**
  - Description: See room-by-room lighting analysis
  - Pre-condition: CAD file processed successfully
  - Post-condition: Analysis data displayed
  - Includes: View Fixture Recommendations

- **Select Alternative Fixture**
  - Description: Choose different fixture from recommendations
  - Pre-condition: Analysis results available
  - Post-condition: Fixture selection updated, cost recalculated

- **Generate Report**
  - Description: Create PDF or CSV report
  - Pre-condition: Analysis results available
  - Post-condition: Report file generated and downloaded

- **View Project History**
  - Description: Browse past projects
  - Pre-condition: Must be logged in
  - Post-condition: Project list displayed

- **Browse Lighting Catalog**
  - Description: View available fixtures
  - Pre-condition: None
  - Post-condition: Catalog displayed

- **Logout**
  - Description: End user session
  - Pre-condition: Must be logged in
  - Post-condition: Session terminated

#### Administrator Use Cases:
- **Manage Users**
  - Description: Create, edit, delete user accounts
  - Pre-condition: Admin privileges
  - Post-condition: User records modified

- **Manage Lighting Catalog**
  - Description: Add, edit, remove fixtures
  - Pre-condition: Admin privileges
  - Post-condition: Catalog updated

- **View System Logs**
  - Description: Access system activity logs
  - Pre-condition: Admin privileges
  - Post-condition: Logs displayed

- **Configure System Settings**
  - Description: Modify application parameters
  - Pre-condition: Admin privileges
  - Post-condition: Settings updated

#### Vendor Use Cases:
- **View Catalog**
  - Description: Browse fixture database
  - Pre-condition: Vendor account
  - Post-condition: Catalog displayed

- **View Project Reports** (Limited)
  - Description: Access specific project reports
  - Pre-condition: Permission granted
  - Post-condition: Report displayed

### Relationships

**Generalization**:
- Architect, Administrator, Vendor **IS-A** Registered User
- Registered User **IS-A** Guest User (after registration)

**Include**:
- "View Analysis Results" **includes** "View Fixture Recommendations"
- "Generate Report" **includes** "Calculate Total Cost"

**Extend**:
- "Provide Symbol Legend" **extends** "Upload CAD File"
- "Apply Custom Room Type" **extends** "View Analysis Results"

### Draw.io Instructions

1. Create a rectangle representing the system boundary labeled "AutoLight Analyser"
2. Add stick figure actors on the left side: Guest User, Architect, Admin, Vendor
3. Draw ovals inside the system boundary for each use case
4. Connect actors to use cases with solid lines
5. Use dashed arrows for «include» and «extend» relationships
6. Use hollow triangular arrows for generalization relationships

---

## 2. CLASS DIAGRAM

### Description
The Class Diagram shows the object-oriented structure of the AutoLight Analyser system, including classes, attributes, methods, and relationships.

### Classes

#### 1. User (Django Built-in)
```
┌─────────────────────────┐
│       «Model»           │
│         User            │
├─────────────────────────┤
│ - id: Integer           │
│ - username: String      │
│ - email: String         │
│ - password: String      │
│ - first_name: String    │
│ - last_name: String     │
│ - date_joined: DateTime │
│ - is_active: Boolean    │
├─────────────────────────┤
│ + authenticate()        │
│ + set_password()        │
│ + get_full_name()       │
└─────────────────────────┘
```

#### 2. LightingCatalog
```
┌─────────────────────────────┐
│          «Model»            │
│      LightingCatalog        │
├─────────────────────────────┤
│ - id: Integer (PK)          │
│ - symbol_name: String       │
│ - model_number: String      │
│ - brand: String             │
│ - lumens: Integer           │
│ - wattage: Float            │
│ - beam_angle: Float         │
│ - color_temp: Integer       │
│ - unit_cost: Decimal (INR)  │
│ - image: ImageField         │
│ - created_at: DateTime      │
│ - updated_at: DateTime      │
├─────────────────────────────┤
│ + __str__(): String         │
│ + save(): void              │
└─────────────────────────────┘
```

#### 3. CADFile
```
┌─────────────────────────────┐
│          «Model»            │
│          CADFile            │
├─────────────────────────────┤
│ - id: Integer (PK)          │
│ - user: ForeignKey(User)    │
│ - project_name: String      │
│ - filename: String          │
│ - file: FileField           │
│ - status: String            │
│   ['pending', 'processing', │
│    'completed', 'failed']   │
│ - uploaded_at: DateTime     │
│ - processed_at: DateTime    │
│ - error_message: Text       │
├─────────────────────────────┤
│ + __str__(): String         │
└─────────────────────────────┘
```

#### 4. Room
```
┌─────────────────────────────┐
│          «Model»            │
│           Room              │
├─────────────────────────────┤
│ - id: Integer (PK)          │
│ - cad_file: ForeignKey      │
│ - name: String              │
│ - room_type: String         │
│   ['bedroom', 'office',     │
│    'kitchen', 'showroom'..] │
│ - length: Float (nullable)  │
│ - width: Float (nullable)   │
│ - area: Float               │
│ - height: Float             │
│ - required_lux: Float       │
├─────────────────────────────┤
│ + LUX_STANDARDS: Dict       │
│ + save(): void              │
│ + clean(): void             │
│ + calculate_required_lux()  │
│ + calculate_required_lumens()│
│ + total_lumens_required     │
│   (property)                │
│ + current_lux (property)    │
│ + is_adequately_lit         │
│   (property)                │
│ + __str__(): String         │
└─────────────────────────────┘
```

#### 5. Fixture
```
┌─────────────────────────────┐
│          «Model»            │
│          Fixture            │
├─────────────────────────────┤
│ - id: Integer (PK)          │
│ - room: ForeignKey(Room)    │
│ - lighting_catalog:         │
│   ForeignKey(Catalog)       │
│ - quantity: Integer         │
│ - x_coordinate: Float       │
│ - y_coordinate: Float       │
├─────────────────────────────┤
│ + total_lumens (property)   │
│ + total_cost (property)     │
│ + __str__(): String         │
└─────────────────────────────┘
```

#### 6. Report
```
┌─────────────────────────────┐
│          «Model»            │
│          Report             │
├─────────────────────────────┤
│ - id: Integer (PK)          │
│ - cad_file: ForeignKey      │
│ - report_type: String       │
│   ['pdf', 'csv']            │
│ - file_path: FileField      │
│ - generated_at: DateTime    │
├─────────────────────────────┤
│ + __str__(): String         │
└─────────────────────────────┘
```

#### 7. CADParser (Utility Class)
```
┌─────────────────────────────┐
│         «Utility»           │
│         CADParser           │
├─────────────────────────────┤
│ (No attributes - stateless) │
├─────────────────────────────┤
│ + parse_cad(file_path):     │
│   Dict                      │
│ + extract_blocks():         │
│   List[Dict]                │
│ + extract_polylines():      │
│   List[Dict]                │
│ + calculate_polyline_area():│
│   Float                     │
└─────────────────────────────┘
```

#### 8. LightingCalculator (Utility Class)
```
┌─────────────────────────────┐
│         «Utility»           │
│    LightingCalculator       │
├─────────────────────────────┤
│ (No attributes - stateless) │
├─────────────────────────────┤
│ + calculate_required_lux(): │
│   Float                     │
│ + calculate_current_lux():  │
│   Float                     │
│ + calculate_fixture_count():│
│   Integer                   │
│ + calculate_efficiency():   │
│   Float                     │
└─────────────────────────────┘
```

#### 9. RecommendationEngine (Utility Class)
```
┌─────────────────────────────┐
│         «Utility»           │
│   RecommendationEngine      │
├─────────────────────────────┤
│ (No attributes - stateless) │
├─────────────────────────────┤
│ + get_budget_based_rec():   │
│   List[LightingCatalog]     │
│ + calculate_efficiency():   │
│   Float                     │
│ + sort_by_relevance():      │
│   List[LightingCatalog]     │
└─────────────────────────────┘
```

#### 10. ReportGenerator (Utility Class)
```
┌─────────────────────────────┐
│         «Utility»           │
│      ReportGenerator        │
├─────────────────────────────┤
│ (No attributes - stateless) │
├─────────────────────────────┤
│ + generate_pdf(cad_file):   │
│   String                    │
│ + generate_csv(cad_file):   │
│   String                    │
│ + create_summary_table():   │
│   Table                     │
└─────────────────────────────┘
```

### Relationships

#### Associations (with Multiplicity):

1. **User → CADFile**
   - Type: One-to-Many
   - Multiplicity: 1 User has 0..* CADFiles
   - FK: CADFile.user → User.id

2. **CADFile → Room**
   - Type: One-to-Many
   - Multiplicity: 1 CADFile has 1..* Rooms
   - FK: Room.cad_file → CADFile.id

3. **Room → Fixture**
   - Type: One-to-Many
   - Multiplicity: 1 Room has 0..* Fixtures
   - FK: Fixture.room → Room.id

4. **LightingCatalog → Fixture**
   - Type: One-to-Many
   - Multiplicity: 1 LightingCatalog appears in 0..* Fixtures
   - FK: Fixture.lighting_catalog → LightingCatalog.id

5. **CADFile → Report**
   - Type: One-to-Many
   - Multiplicity: 1 CADFile has 0..* Reports
   - FK: Report.cad_file → CADFile.id

#### Dependencies:

- **CADParser** depends on **CADFile** (uses file path)
- **LightingCalculator** depends on **Room** and **Fixture**
- **RecommendationEngine** depends on **LightingCatalog**
- **ReportGenerator** depends on **CADFile**, **Room**, **Fixture**

### Draw.io Instructions

1. Create rectangles divided into three sections for each class
2. Top section: Class name (centered, bold)
3. Middle section: Attributes (with types)
4. Bottom section: Methods (with return types)
5. Draw solid lines with diamond for composition (User ◆—— CADFile)
6. Draw hollow diamond for aggregation
7. Use arrows for dependencies (dashed lines)
8. Add multiplicity labels on association lines (1, 0..*, 1..*)

---

## 3. SEQUENCE DIAGRAM

### Description
The Sequence Diagram shows the interaction flow for the main use case: "Upload and Process CAD File".

### Actors and Objects

- **Actor**: Architect (User)
- **Objects**:
  1. Browser (Frontend)
  2. UploadView (Django View)
  3. CADFile (Model)
  4. CADParser (Utility)
  5. Room (Model)
  6. Fixture (Model)
  7. SymbolMapper (Utility)
  8. LightingCatalog (Model)
  9. LightingCalculator (Utility)
  10. Database

### Interaction Flow

```
Sequence: CAD File Upload and Processing

Architect → Browser: 
    1. Navigate to /upload page
    
Browser → UploadView: 
    2. GET /upload/
    
UploadView → Browser: 
    3. Return upload form HTML
    
Architect → Browser: 
    4. Fill form (project name, select .dxf file)
    5. Click "Upload" button
    
Browser → UploadView: 
    6. POST /upload/ (multipart/form-data)
    
UploadView → CADFile: 
    7. Create CADFile object
    7a. Set status = 'pending'
    7b. Set user = current_user
    7c. Set filename
    
CADFile → Database: 
    8. save() - INSERT INTO cad_files
    
Database → CADFile: 
    9. Return id
    
UploadView → CADFile: 
    10. Update status = 'processing'
    
CADFile → Database: 
    11. save() - UPDATE cad_files
    
UploadView → CADParser: 
    12. parse_cad(file_path)
    
CADParser → CADParser: 
    13. Open file with ezdxf
    14. Extract INSERT blocks
    15. Extract LWPOLYLINE entities
    
CADParser → UploadView: 
    16. Return {blocks: [...], rooms: [...]}
    
UploadView → Room: 
    17. Loop: For each room_data in parsed.rooms
    
Room → Room: 
    18. Calculate area from polyline points
    19. Validate area (0.1 m² to 10,000 m²)
    
Room → Database: 
    20. save() - INSERT INTO rooms
    
UploadView → SymbolMapper: 
    21. map_symbols_to_catalog(block_names, legend)
    
SymbolMapper → LightingCatalog: 
    22. Query catalog for matching symbols
    
LightingCatalog → Database: 
    23. SELECT * FROM lighting_catalog WHERE symbol_name = ?
    
Database → LightingCatalog: 
    24. Return matching catalog items
    
LightingCatalog → SymbolMapper: 
    25. Return catalog objects
    
SymbolMapper → UploadView: 
    26. Return {symbol: catalog_item} mapping
    
UploadView → Fixture: 
    27. Loop: For each mapped symbol
    
Fixture → Fixture: 
    28. Set quantity = count of blocks
    29. Set coordinates from first block
    
Fixture → Database: 
    30. save() - INSERT INTO fixtures
    
UploadView → Room: 
    31. For each room, calculate required lux
    
Room → LightingCalculator: 
    32. calculate_required_lumens(area, room_type)
    
LightingCalculator → Room: 
    33. Return required_lumens
    
Room → Fixture: 
    34. Get all fixtures in room
    
Fixture → Database: 
    35. SELECT * FROM fixtures WHERE room_id = ?
    
Database → Fixture: 
    36. Return fixture list
    
Fixture → Room: 
    37. Return fixtures
    
Room → LightingCalculator: 
    38. calculate_current_lux(fixtures, area)
    
LightingCalculator → Room: 
    39. Return current_lux
    
Room → Database: 
    40. save() - UPDATE rooms SET current_lux
    
UploadView → CADFile: 
    41. Update status = 'completed'
    42. Set processed_at = now()
    
CADFile → Database: 
    43. save() - UPDATE cad_files
    
UploadView → Browser: 
    44. HTTP 302 Redirect to /results/{cad_id}/
    
Browser → Architect: 
    45. Display success message
    46. Load results page
```

### Alternative Flow (Error Scenario)

```
If parsing fails at step 13:

CADParser → UploadView: 
    13a. Raise Exception("Invalid CAD file format")
    
UploadView → CADFile: 
    14a. Set status = 'failed'
    15a. Set error_message = exception details
    
CADFile → Database: 
    16a. save() - UPDATE cad_files
    
UploadView → Browser: 
    17a. Return error page with message
    
Browser → Architect: 
    18a. Display error notification
```

### Draw.io Instructions

1. Create vertical lifelines for each object/actor
2. Draw horizontal arrows for messages (method calls)
3. Label each arrow with sequence number and message name
4. Use solid arrows for synchronous calls
5. Use dashed arrows for return messages
6. Add activation boxes (thin rectangles) on lifelines during processing
7. Use alt/opt frames for conditional logic
8. Add loop frames for iteration

---

## 4. DATA FLOW DIAGRAM - LEVEL 0 (CONTEXT DIAGRAM)

### Description
The Level 0 DFD shows the AutoLight Analyser system as a single process with external entities and major data flows.

### External Entities

1. **Architect** (User)
   - Uploads CAD files
   - Views reports
   - Manages projects

2. **Administrator**
   - Manages catalog
   - Configures system
   - Views logs

3. **File System**
   - Stores uploaded CAD files
   - Stores generated reports
   - Stores fixture images

4. **Lighting Catalog Database**
   - Contains fixture specifications
   - Provides product data

### Central Process

**Process 0: AutoLight Analyser System**

### Data Flows

#### Input Flows (from entities to system):

1. **Architect → System**:
   - User credentials
   - CAD file (.dwg/.dxf)
   - Project metadata (name, description)
   - Optional symbol legend
   - Fixture selection changes
   - Report generation requests

2. **Administrator → System**:
   - Admin credentials
   - Fixture catalog updates
   - System configuration changes
   - User management commands

3. **File System → System**:
   - Stored CAD files (for processing)
   - Previously generated reports

4. **Lighting Catalog Database → System**:
   - Fixture specifications
   - Product pricing (INR)
   - Technical parameters

#### Output Flows (from system to entities):

1. **System → Architect**:
   - Authentication status
   - Dashboard statistics
   - Room analysis results
   - Fixture recommendations
   - Current vs required lux data
   - Cost calculations
   - PDF reports
   - CSV reports
   - Success/error messages

2. **System → Administrator**:
   - System status
   - User activity logs
   - Catalog management interface
   - Configuration confirmations

3. **System → File System**:
   - Uploaded CAD files
   - Generated PDF reports
   - Generated CSV reports
   - Processed data backups

4. **System → Lighting Catalog Database**:
   - New fixture entries
   - Updated pricing
   - Modified specifications

### Diagram Structure (Textual Representation)

```
                    User Credentials
                    CAD Files
                    Project Data          
         ┌──────────────────────────────►
         │
         │        Authentication Status
         │        Analysis Results
         │        Reports
    [Architect] ◄────────────────────────
         │
         │
         ▼
    ┌────────────────────────────────┐
    │                                │
    │    Process 0                   │
    │    AutoLight Analyser          │
    │    System                      │
    │                                │
    └────────────────────────────────┘
         ▲                    │
         │                    │
         │ Fixture Data       │ Report Files
         │ Specs & Pricing    │ CAD Files
         │                    ▼
    [Lighting Catalog]    [File System]
    [Database]
         ▲
         │
         │ Catalog Updates
         │ System Config
         │
    [Administrator]
```

### Draw.io Instructions

1. Draw a large circle in the center labeled "0 AutoLight Analyser System"
2. Draw rectangles for external entities (Architect, Admin, File System, Database)
3. Draw labeled arrows for each data flow
4. Use different colors for input and output flows
5. Make sure arrow labels clearly describe the data being transferred

---

## 5. DATA FLOW DIAGRAM - LEVEL 1 (DETAILED PROCESSES)

### Description
The Level 1 DFD decomposes the AutoLight Analyser system into major sub-processes with data stores.

### Processes

1. **Process 1.0: User Authentication**
   - Input: Login credentials
   - Output: Session token, user role
   - Data Store: User database

2. **Process 2.0: CAD File Upload & Validation**
   - Input: CAD file, project metadata
   - Output: Validated file, CADFile record
   - Data Store: CAD Files storage, CADFile database

3. **Process 3.0: CAD Parsing**
   - Input: CAD file path
   - Output: Extracted blocks, polylines
   - Data Store: Temporary parsing data

4. **Process 4.0: Room Detection & Area Calculation**
   - Input: Polyline data
   - Output: Room records with dimensions
   - Data Store: Room database

5. **Process 5.0: Symbol-to-Catalog Mapping**
   - Input: Block symbols, legend
   - Output: Fixture mappings
   - Data Store: Lighting Catalog database

6. **Process 6.0: Fixture Assignment**
   - Input: Mapped fixtures, room IDs
   - Output: Fixture records
   - Data Store: Fixture database

7. **Process 7.0: Lighting Analysis**
   - Input: Room data, fixtures
   - Output: Lux calculations, adequacy status
   - Data Store: Room database

8. **Process 8.0: Recommendation Generation**
   - Input: Current fixtures, budget
   - Output: Alternative fixtures
   - Data Store: Lighting Catalog database

9. **Process 9.0: Report Generation**
   - Input: Analysis results
   - Output: PDF/CSV reports
   - Data Store: Report files, Report database

### Data Stores

- **D1: User Database** - User accounts, roles, sessions
- **D2: CADFile Database** - Project metadata, processing status
- **D3: Room Database** - Room dimensions, lux requirements
- **D4: Fixture Database** - Installed fixtures, quantities
- **D5: Lighting Catalog Database** - Available fixtures, specifications
- **D6: Report Database** - Generated report metadata
- **D7: CAD Files Storage** - Uploaded .dwg/.dxf files
- **D8: Report Files Storage** - Generated PDF/CSV files

### Data Flow Connections

```
[Architect]
    │
    ├─► (1.0 User Authentication) ◄──► [D1: User DB]
    │       │
    │       ▼ (authenticated)
    │
    ├─► (2.0 CAD Upload & Validation)
    │       │
    │       ├──► [D2: CADFile DB]
    │       └──► [D7: CAD Files Storage]
    │       │
    │       ▼ (validated file)
    │
    ├─► (3.0 CAD Parsing)
    │       │
    │       ◄──── [D7: CAD Files Storage]
    │       │
    │       ├──► blocks data
    │       └──► polyline data
    │       │
    │       ▼
    │   ┌───────────────────────┐
    │   │                       │
    │   ▼                       ▼
    │ (4.0 Room Detection)   (5.0 Symbol Mapping)
    │   │                       │
    │   ├──► [D3: Room DB]     ├──► [D5: Catalog DB]
    │   │                       │
    │   ▼                       ▼
    │ room records          fixture mappings
    │   │                       │
    │   └───────┬───────────────┘
    │           │
    │           ▼
    │      (6.0 Fixture Assignment)
    │           │
    │           ├──► [D4: Fixture DB]
    │           │
    │           ▼
    │      ┌────────────────┐
    │      │                │
    │      ▼                ▼
    │  (7.0 Lighting   (8.0 Recommendation
    │    Analysis)        Generation)
    │      │                │
    │      ◄────┐      ◄────┘
    │      │    │      │
    │      │  [D3]   [D5]
    │      │    │      │
    │      ▼    │      │
    │    lux    │      │
    │  results  │      │
    │      │    │      │
    │      └────┴──────┘
    │           │
    │           ▼
    │      (9.0 Report Generation)
    │           │
    │           ├──► [D6: Report DB]
    │           ├──► [D8: Report Files]
    │           │
    │           ▼
    └───────── reports
    
[Administrator]
    │
    ├─► (1.0 User Authentication) ◄──► [D1: User DB]
    │       │
    │       ▼
    │
    └─► Catalog Management ◄──► [D5: Catalog DB]
```

### Detailed Process Descriptions

#### Process 2.0: CAD File Upload & Validation

**Inputs**:
- CAD file (from Architect)
- Project name (from Architect)
- Optional legend (from Architect)

**Processing**:
1. Validate file format (.dwg or .dxf)
2. Check file size constraints
3. Create CADFile database record
4. Set status = 'pending'
5. Save file to storage
6. Return file ID

**Outputs**:
- CADFile record (to D2: CADFile DB)
- Stored file (to D7: CAD Files Storage)
- Upload confirmation (to Architect)

**Data Stores Used**:
- Read/Write: D2 (CADFile DB)
- Write: D7 (CAD Files Storage)

#### Process 3.0: CAD Parsing

**Inputs**:
- CAD file path (from D7: CAD Files Storage)
- CADFile ID (from Process 2.0)

**Processing**:
1. Update CADFile status = 'processing'
2. Open file with ezdxf library
3. Extract INSERT blocks (fixtures)
   - Block name
   - X, Y, Z coordinates
   - Rotation angle
   - Layer information
4. Extract LWPOLYLINE entities (rooms)
   - Boundary points
   - Layer information
5. Handle parsing errors

**Outputs**:
- Block data list (to Process 5.0)
- Polyline data list (to Process 4.0)
- Parsing errors (to Architect if failed)

**Data Stores Used**:
- Read: D7 (CAD Files Storage)
- Read/Write: D2 (CADFile DB)

#### Process 4.0: Room Detection & Area Calculation

**Inputs**:
- Polyline data (from Process 3.0)
- CADFile ID

**Processing**:
1. For each closed polyline:
   - Apply Shoelace formula to calculate area
   - Convert from mm² to m²
   - Validate area (0.1 m² to 10,000 m²)
2. Assign default room types
3. Calculate required lux based on type
4. Create Room database records

**Outputs**:
- Room records (to D3: Room DB)
- Room IDs (to Process 6.0)

**Data Stores Used**:
- Write: D3 (Room DB)

#### Process 5.0: Symbol-to-Catalog Mapping

**Inputs**:
- Block data (from Process 3.0)
- Optional legend (from Architect)

**Processing**:
1. Extract unique block names
2. For each symbol:
   - Apply legend translation if provided
   - Try exact match with catalog symbol_name
   - Try fuzzy match (first 3 characters)
   - Mark as unmapped if no match
3. Create symbol-to-catalog mapping

**Outputs**:
- Fixture mappings (to Process 6.0)
- Unmapped symbols list (to Architect as warning)

**Data Stores Used**:
- Read: D5 (Lighting Catalog DB)

#### Process 6.0: Fixture Assignment

**Inputs**:
- Room IDs (from Process 4.0)
- Fixture mappings (from Process 5.0)
- Block coordinates (from Process 3.0)

**Processing**:
1. Group blocks by symbol name
2. Count quantity for each symbol type
3. For each mapped fixture:
   - Create Fixture record
   - Link to appropriate Room
   - Link to LightingCatalog entry
   - Set quantity and coordinates
4. Distribute fixtures across rooms

**Outputs**:
- Fixture records (to D4: Fixture DB)
- Fixture IDs (to Process 7.0 and 8.0)

**Data Stores Used**:
- Read: D3 (Room DB)
- Write: D4 (Fixture DB)
- Read: D5 (Lighting Catalog DB)

#### Process 7.0: Lighting Analysis

**Inputs**:
- Room records (from D3: Room DB)
- Fixture records (from D4: Fixture DB)

**Processing**:
1. For each room:
   - Calculate total installed lumens
   - Apply efficiency factor (0.7)
   - Calculate current lux = lumens / area
   - Compare to required lux
   - Determine adequacy status
2. Update Room records with calculations

**Outputs**:
- Updated Room records with lux data (to D3: Room DB)
- Analysis results (to Process 9.0)
- Results display (to Architect)

**Data Stores Used**:
- Read/Write: D3 (Room DB)
- Read: D4 (Fixture DB)

#### Process 8.0: Recommendation Generation

**Inputs**:
- Current fixture data (from D4: Fixture DB)
- Lighting catalog (from D5: Lighting Catalog DB)

**Processing**:
1. For each installed fixture:
   - Calculate budget thresholds (±20%)
   - Query similar fixtures by lumens (±25%)
   - Filter by price ranges:
     * Below budget (70-100%)
     * Within budget (80-120%)
     * Above budget (100-130%)
   - Calculate efficiency scores
   - Sort by relevance
2. Return top 10 recommendations per fixture

**Outputs**:
- Recommendations list (to Architect)
- Recommendation data (to Process 9.0)

**Data Stores Used**:
- Read: D4 (Fixture DB)
- Read: D5 (Lighting Catalog DB)

#### Process 9.0: Report Generation

**Inputs**:
- CADFile ID
- Analysis results (from Process 7.0)
- Recommendation data (from Process 8.0)

**Processing**:
1. Gather all project data:
   - Project metadata
   - Room details
   - Fixture specifications
   - Cost calculations
   - Lux analysis results
2. Generate PDF report:
   - Format with ReportLab
   - Include tables and summaries
   - Apply professional styling
3. Generate CSV report:
   - Export structured data
   - Include all numeric values
4. Create Report database record

**Outputs**:
- PDF file (to D8: Report Files Storage)
- CSV file (to D8: Report Files Storage)
- Report record (to D6: Report DB)
- Download links (to Architect)

**Data Stores Used**:
- Read: D2 (CADFile DB)
- Read: D3 (Room DB)
- Read: D4 (Fixture DB)
- Write: D6 (Report DB)
- Write: D8 (Report Files Storage)

### Draw.io Instructions

1. Draw circles for each process (numbered 1.0 to 9.0)
2. Draw open-ended rectangles for data stores (labeled D1 to D8)
3. Draw rectangles for external entities (Architect, Administrator)
4. Connect with labeled arrows showing data flows
5. Use different arrow styles for read vs. write operations
6. Group related processes with dashed boundaries

---

## 6. DEPLOYMENT DIAGRAM

### Description
The Deployment Diagram shows the physical architecture of the AutoLight Analyser system in a production environment.

### Nodes (Hardware/Infrastructure)

1. **Client Devices**
   - Type: Execution environment
   - Description: User devices (laptops, desktops, tablets)
   - Components: Web browsers (Chrome, Firefox, Safari, Edge)

2. **Load Balancer / Reverse Proxy Server**
   - Type: Device
   - Description: Nginx server
   - IP: Public-facing
   - Responsibilities:
     - SSL/TLS termination
     - Request routing
     - Static file serving
     - Load distribution

3. **Application Server(s)**
   - Type: Device (multiple instances for scalability)
   - Description: Ubuntu 22.04 LTS servers
   - Components:
     - Gunicorn WSGI server
     - Django application
     - Python 3.12 runtime

4. **Task Queue Server**
   - Type: Device
   - Description: Ubuntu server
   - Components:
     - Redis server (message broker)
     - Celery workers

5. **Database Server**
   - Type: Device
   - Description: PostgreSQL database server
   - Components:
     - PostgreSQL 14+
     - Connection pooler (pgBouncer)

6. **File Storage Server**
   - Type: Device
   - Description: Network file system
   - Components:
     - CAD files storage
     - Report files storage
     - Media assets storage

### Communication Protocols

- **HTTPS (443)**: Client ↔ Load Balancer
- **HTTP (80)**: Load Balancer ↔ Application Servers
- **PostgreSQL (5432)**: Application Servers ↔ Database Server
- **Redis (6379)**: Application Servers ↔ Task Queue
- **NFS/SMB**: Application Servers ↔ File Storage

### Component Deployment

```
┌─────────────────────────────────────┐
│       Client Tier                   │
│   ┌──────────┐  ┌──────────┐       │
│   │ Browser  │  │  Mobile  │       │
│   │ (Chrome) │  │ (Safari) │       │
│   └──────────┘  └──────────┘       │
└─────────────────┬───────────────────┘
                  │ HTTPS (443)
                  │
┌─────────────────▼───────────────────┐
│   Load Balancer Server              │
│   ┌─────────────────────────────┐   │
│   │  Nginx                      │   │
│   │  - SSL Certificate          │   │
│   │  - Reverse Proxy            │   │
│   │  - Static File Cache        │   │
│   └─────────────────────────────┘   │
└─────────────┬───────────────────────┘
              │ HTTP (80)
              │
   ┌──────────┴───────────┐
   │                      │
┌──▼─────────────┐  ┌────▼──────────────┐
│ App Server 1   │  │  App Server 2     │
│ ┌────────────┐ │  │ ┌────────────┐   │
│ │ Gunicorn   │ │  │ │ Gunicorn   │   │
│ │ (4 workers)│ │  │ │ (4 workers)│   │
│ ├────────────┤ │  │ ├────────────┤   │
│ │ Django App │ │  │ │ Django App │   │
│ │ - Views    │ │  │ │ - Views    │   │
│ │ - Models   │ │  │ │ - Models   │   │
│ │ - Utils    │ │  │ │ - Utils    │   │
│ └────────────┘ │  │ └────────────┘   │
└──┬─────────┬───┘  └──┬─────────┬─────┘
   │         │         │         │
   │         └─────────┴─────────┘
   │                   │
   │                   │ PostgreSQL (5432)
   │                   │
   │         ┌─────────▼──────────┐
   │         │  Database Server   │
   │         │ ┌────────────────┐ │
   │         │ │ PostgreSQL 14  │ │
   │         │ │ - user DB      │ │
   │         │ │ - cad_file DB  │ │
   │         │ │ - room DB      │ │
   │         │ │ - fixture DB   │ │
   │         │ │ - catalog DB   │ │
   │         │ └────────────────┘ │
   │         │ ┌────────────────┐ │
   │         │ │  pgBouncer     │ │
   │         │ │ (Connection    │ │
   │         │ │  Pooling)      │ │
   │         │ └────────────────┘ │
   │         └────────────────────┘
   │
   │ Redis (6379)
   │
   │         ┌──────────────────────┐
   └────────►│ Task Queue Server    │
             │ ┌──────────────────┐ │
             │ │ Redis (Broker)   │ │
             │ └──────────────────┘ │
             │ ┌──────────────────┐ │
             │ │ Celery Worker 1  │ │
             │ │ - CAD Processing │ │
             │ └──────────────────┘ │
             │ ┌──────────────────┐ │
             │ │ Celery Worker 2  │ │
             │ │ - Report Gen     │ │
             │ └──────────────────┘ │
             └──────────────────────┘
                       │
                       │ NFS/SMB
                       │
             ┌─────────▼────────────┐
             │ File Storage Server  │
             │ ┌──────────────────┐ │
             │ │ /media/          │ │
             │ │ ├─ cad_files/    │ │
             │ │ ├─ reports/      │ │
             │ │ └─ fixtures/     │ │
             │ └──────────────────┘ │
             │ ┌──────────────────┐ │
             │ │ Backup Storage   │ │
             │ └──────────────────┘ │
             └──────────────────────┘
```

### Software Components by Server

#### Load Balancer Server:
- Nginx 1.22+
- SSL/TLS certificates (Let's Encrypt)
- Configuration files:
  - `/etc/nginx/sites-available/autolight`
  - `/etc/nginx/nginx.conf`

#### Application Servers:
- Ubuntu 22.04 LTS
- Python 3.12
- Django 6.0
- Gunicorn 21.x
- System services:
  - autolight.service (systemd)
- Dependencies: ezdxf, ReportLab, Pillow

#### Task Queue Server:
- Ubuntu 22.04 LTS
- Redis 6.x
- Celery 5.x
- System services:
  - redis-server.service
  - celery-worker.service

#### Database Server:
- Ubuntu 22.04 LTS
- PostgreSQL 14
- pgBouncer (connection pooling)
- Backup tools: pg_dump

#### File Storage Server:
- NFS or SMB file server
- Directory structure:
  - `/storage/media/cad_files/`
  - `/storage/media/reports/`
  - `/storage/media/fixtures/`
  - `/storage/backups/`

### Scaling Considerations

**Horizontal Scaling**:
- Add more Application Servers
- Load balancer distributes requests evenly
- Stateless application design enables easy scaling

**Vertical Scaling**:
- Increase CPU/RAM on existing servers
- Optimize database queries
- Add database read replicas

**High Availability**:
- Multiple Application Server instances
- Database replication (primary-replica)
- Redis Sentinel for queue reliability
- Load balancer health checks

---

## 7. COMPONENT DIAGRAM

### Description
The Component Diagram illustrates the software components, their interfaces, and dependencies within the AutoLight Analyser system.

### Components

#### Frontend Layer

1. **React UI Framework**
   - Subcomponents:
     - Dashboard Component
     - Upload Component
     - Results Component
     - Profile Component
     - Layout Component
   - Dependencies: React 18, TypeScript
   - Exports: User interface

2. **Visualization Library**
   - Component: Chart.js wrapper
   - Subcomponents:
     - Bar Chart (fixtures per room)
     - Pie Chart (fixture distribution)
     - Line Chart (lux trends)
   - Dependencies: Chart.js, react-chartjs-2
   - Exports: Data visualizations

3. **PDF Export Module**
   - Component: html2pdf.js integration
   - Function: Client-side PDF generation
   - Exports: PDF generation interface

#### Backend Layer

1. **Django Core Framework**
   - Subcomponents:
     - URL Dispatcher
     - Middleware Stack
     - Template Engine
     - ORM Layer
   - Dependencies: Django 6.0
   - Exports: Web framework services

2. **Authentication Module**
   - Component: Django Auth
   - Functions:
     - User login/logout
     - Session management
     - Permission checks
   - Dependencies: Django Core
   - Exports: Authentication API

3. **CAD Processing Module**
   - Component: CAD Parser
   - Functions:
     - File format validation
     - Block extraction
     - Polyline parsing
   - Dependencies: ezdxf library
   - Exports: Parsed CAD data

4. **Lighting Calculator Module**
   - Component: Lighting Analysis Engine
   - Functions:
     - Lux calculation
     - Lumens calculation
     - Fixture requirement estimation
   - Dependencies: math library
   - Exports: Lighting calculation API

5. **Recommendation Engine Module**
   - Component: Budget-Based Recommender
   - Functions:
     - Budget range filtering
     - Similarity matching
     - Efficiency scoring
   - Dependencies: Django ORM
   - Exports: Recommendation API

6. **Report Generator Module**
   - Component: Report Builder
   - Subcomponents:
     - PDF Generator (ReportLab)
     - CSV Generator (Python CSV)
   - Dependencies: ReportLab, CSV library
   - Exports: Report files

7. **Task Queue Module**
   - Component: Celery Integration
   - Functions:
     - Async CAD processing
     - Background report generation
   - Dependencies: Celery, Redis
   - Exports: Task submission API

#### Data Access Layer

1. **ORM Models**
   - Components:
     - User Model
     - CADFile Model
     - Room Model
     - Fixture Model
     - LightingCatalog Model
     - Report Model
   - Dependencies: Django Models
   - Exports: Database abstraction

2. **Database Driver**
   - Component: PostgreSQL adapter
   - Function: SQL execution
   - Dependencies: psycopg2
   - Exports: Database connection

#### External Integrations

1. **File Storage**
   - Component: Django File Storage
   - Functions:
     - CAD file storage
     - Report storage
     - Media management
   - Exports: File I/O interface

### Component Relationships

```
┌─────────────────────────────────────────────────┐
│               Frontend Layer                    │
│                                                 │
│  ┌────────────┐     ┌─────────────────────┐   │
│  │ React UI   │◄────┤ Visualization Lib   │   │
│  │ Framework  │     │ (Chart.js)          │   │
│  └─────┬──────┘     └─────────────────────┘   │
│        │                                        │
│        │ HTTP/AJAX                              │
└────────┼────────────────────────────────────────┘
         │
         │
┌────────▼────────────────────────────────────────┐
│              Backend Layer                      │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │        Django Core Framework            │   │
│  │  ┌───────────┐   ┌────────────────┐    │   │
│  │  │    URL    │   │   Middleware   │    │   │
│  │  │ Dispatcher│   │     Stack      │    │   │
│  │  └───────────┘   └────────────────┘    │   │
│  └────────┬──────────────────┬─────────────┘   │
│           │                  │                  │
│           │                  │                  │
│  ┌────────▼─────┐   ┌───────▼──────────────┐  │
│  │ Authentication│   │    View Layer        │  │
│  │    Module     │   │  - dashboard()       │  │
│  │               │◄──┤  - upload_cad()      │  │
│  └───────────────┘   │  - results()         │  │
│                      │  - generate_report() │  │
│                      └──┬──────────┬────────┘  │
│                         │          │            │
│        ┌────────────────┘          └─────────┐ │
│        │                                     │ │
│  ┌─────▼──────┐   ┌──────────┐   ┌─────────▼┐ │
│  │    CAD     │   │ Lighting │   │Recommenda││ │
│  │ Processing │   │Calculator│   │   tion   ││ │
│  │   Module   │   │  Module  │   │  Engine  ││ │
│  └────────────┘   └──────────┘   └──────────┘ │
│        │                  │              │     │
│        └──────────┬───────┴──────────────┘     │
│                   │                             │
│           ┌───────▼────────┐                   │
│           │  Report        │                   │
│           │  Generator     │                   │
│           │  Module        │                   │
│           └────────────────┘                   │
│                   │                             │
└───────────────────┼─────────────────────────────┘
                    │
                    │
┌───────────────────▼─────────────────────────────┐
│          Data Access Layer                      │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │           ORM Models                     │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌────────┐ │  │
│  │  │ User │ │ CAD  │ │ Room │ │Fixture │ │  │
│  │  │      │ │ File │ │      │ │        │ │  │
│  │  └──────┘ └──────┘ └──────┘ └────────┘ │  │
│  │  ┌──────────┐ ┌──────────┐             │  │
│  │  │Lighting  │ │ Report   │             │  │
│  │  │ Catalog  │ │          │             │  │
│  │  └──────────┘ └──────────┘             │  │
│  └──────────────────┬───────────────────────┘  │
│                     │                           │
│           ┌─────────▼────────────┐             │
│           │   Database Driver    │             │
│           │   (psycopg2)         │             │
│           └──────────────────────┘             │
└───────────────────┬─────────────────────────────┘
                    │
                    │
┌───────────────────▼─────────────────────────────┐
│           PostgreSQL Database                   │
└─────────────────────────────────────────────────┘
```

### Interface Definitions

**IAuthentication**:
- Methods:
  - login(username, password) → session_token
  - logout(session_token) → boolean
  - verify_session(session_token) → user_object

**ICADParser**:
- Methods:
  - parse_file(file_path) → parsed_data
  - extract_blocks() → block_list
  - extract_rooms() → room_list

**ILightingCalculator**:
- Methods:
  - calculate_required_lux(room_type) → lux_value
  - calculate_current_lux(fixtures, area) → lux_value
  - calculate_fixture_count(area, lumens) → fixture_count

**IRecommendationEngine**:
- Methods:
  - get_recommendations(fixture, budget_range) → fixture_list
  - calculate_efficiency(fixture) → efficiency_score
  - sort_by_relevance(fixtures) → sorted_list

**IReportGenerator**:
- Methods:
  - generate_pdf(cad_file) → file_path
  - generate_csv(cad_file) → file_path

**IOrmModels**:
- Methods:
  - save() → boolean
  - delete() → boolean
  - get(id) → model_instance
  - filter(criteria) → queryset

---

## Summary

These diagrams provide a complete visual specification of the AutoLight Analyser system:

1. **Use Case Diagram**: User interactions and system boundaries
2. **Class Diagram**: Object-oriented design and relationships
3. **Sequence Diagram**: Temporal flow of CAD processing
4. **DFD Level 0**: System context and external entities
5. **DFD Level 1**: Internal processes and data stores
6. **Deployment Diagram**: Physical infrastructure and deployment
7. **Component Diagram**: Software components and interfaces

All diagrams follow standard UML 2.5 and DFD conventions, suitable for:
- Academic documentation
- IEEE-style project reports
- Viva presentations
- Technical specifications

---

**Tools Recommended for Diagram Creation**:
- **Draw.io** (diagrams.net) - Free, web-based, supports all diagram types
- **Lucidchart** - Professional, collaborative, templates available
- **StarUML** - Desktop application, comprehensive UML support
- **PlantUML** - Text-based, version control friendly
- **Microsoft Visio** - Industry standard (paid)

---

**Document Prepared For**: Final Year Engineering Project
**Project Title**: AutoLight Analyser - Intelligent Lighting Recommendation System
**Date**: December 2024

---
