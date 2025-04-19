# Privacy-Preserving Identity Verification System - Frontend Documentation

## Overview

The frontend of the Privacy-Preserving Identity Verification System provides a user-friendly interface for interacting with the privacy-preserving verification features. It offers a secure and intuitive user experience for identity verification, document validation, and privacy management, while interfacing with the blockchain-based backend.

## Key Features

- **Identity Verification**: Facial recognition and document verification interfaces
- **Privacy Dashboard**: Comprehensive overview of user privacy settings and data
- **Homomorphic Encryption Demo**: Interactive demonstration of privacy-preserving data computation
- **GDPR Compliance Tools**: User interfaces for consent management and data subject requests
- **Permission Management**: Control third-party access to verification data
- **Blockchain Integration**: Visualize and interact with blockchain-stored identity data

## Technology Stack

The frontend system is built using the following technologies:

- **Framework**: React.js (18.2.0)
- **UI Component Library**: Material-UI (v4 & v5)
- **Routing**: React Router (v6)
- **API Communication**: Axios
- **State Management**: React Context API
- **Authentication**: Custom Auth Context
- **Blockchain Interaction**: Web3.js and ethers.js libraries
- **Date Handling**: date-fns
- **Containerization**: Docker

## Architecture Overview

```mermaid
graph TD
    User([User]) --> |Interacts with| UI[React UI Components]
    UI --> |Uses| Routes[React Router]
    UI --> |Uses| MaterialUI[Material-UI]
    
    Routes --> |Renders| Pages[Page Components]
    
    Pages --> |Use| Components[Reusable Components]
    Pages --> |Use| ContextAPI[Context Providers]
    Pages --> |Call| Services[API Services]
    
    ContextAPI --> |Provides| AuthContext[Authentication]
    ContextAPI --> |Provides| BlockchainContext[Blockchain]
    
    Services --> |HTTP Requests| Backend[Backend API]
    
    Backend --> |Returns| Responses[API Responses]
    Responses --> |Update| Pages
    
    style User fill:#bbf,stroke:#333,stroke-width:2px
    style UI fill:#f9f,stroke:#333,stroke-width:2px
    style Backend fill:#bfb,stroke:#333,stroke-width:2px
```

## Component Structure

The frontend follows a structured organization of components:

```mermaid
classDiagram
    class App {
        +Routes
        +ThemeProvider
        +Header
        +Footer
    }
    
    class Pages {
        +HomePage
        +VerificationPage
        +ProfilePage
        +PermissionsPage
        +PrivacyDashboardPage
        +HomomorphicEncryptionPage
        +GDPRRequestsPage
    }
    
    class Components {
        +Header
        +Footer
    }
    
    class Contexts {
        +AuthContext
        +BlockchainContext
    }
    
    class Services {
        +authService
        +identityService
        +blockchainService
        +permissionService
        +privacyService
        +encryptionService
        +gdprService
    }
    
    App --> Pages : renders
    App --> Components : uses
    Pages --> Components : use
    Pages --> Contexts : consume
    Pages --> Services : call
```

## Page Components

### Home Page

Serves as the landing page and provides an overview of the system's features.

```mermaid
graph TD
    HomePage --> HeroSection[Hero Section]
    HomePage --> FeatureCards[Feature Cards]
    
    HeroSection --> HeroButtons[Action Buttons]
    FeatureCards --> VerificationCard[Secure Verification]
    FeatureCards --> BlockchainCard[Blockchain Technology]
    FeatureCards --> PrivacyCard[Privacy Protection]
    
    HeroButtons --> VerifyButton[Verify Button]
    HeroButtons --> ProfileButton[Profile Button]
    
    style HomePage fill:#f9f,stroke:#333,stroke-width:2px
```

### Verification Page

Handles facial and document verification processes in a step-by-step flow.

```mermaid
graph TD
    VerificationPage --> Stepper[Verification Stepper]
    
    Stepper --> Step1[Personal Information]
    Stepper --> Step2[Government ID]
    Stepper --> Step3[Biometric Verification]
    Stepper --> Step4[Confirmation]
    
    Step1 --> PersonalForm[Personal Information Form]
    Step2 --> IdUploader[ID Document Uploader]
    Step2 --> IdTypeSelector[Document Type Selector]
    Step3 --> FaceUploader[Facial Image Uploader]
    Step4 --> VerificationSummary[Verification Summary]
    Step4 --> BlockchainDetails[Blockchain Transaction Details]
    
    IdUploader --> OCRExtraction[OCR Data Extraction]
    FaceUploader --> FacialVerification[Facial Verification API]
    IdUploader --> DocumentVerification[Document Verification API]
    
    style VerificationPage fill:#f9f,stroke:#333,stroke-width:2px
```

### Privacy Dashboard Page

Provides a comprehensive overview of privacy settings and data usage.

```mermaid
graph TD
    PrivacyDashboardPage --> PrivacyTabs[Privacy Dashboard Tabs]
    
    PrivacyTabs --> OverviewTab[Overview Tab]
    PrivacyTabs --> ConsentsTab[Consents Tab]
    PrivacyTabs --> DataAccessTab[Data Access Tab]
    PrivacyTabs --> SecurityTab[Security Tab]
    
    OverviewTab --> PrivacyScore[Privacy Score]
    OverviewTab --> PrivacyFeatures[Privacy Features]
    OverviewTab --> ActiveConsents[Active Consents]
    
    ConsentsTab --> ConsentList[Consent List]
    ConsentsTab --> ConsentForm[New Consent Form]
    
    DataAccessTab --> AccessLogs[Access Logs]
    DataAccessTab --> ThirdPartyAccess[Third Party Access]
    
    SecurityTab --> EncryptionStatus[Encryption Status]
    SecurityTab --> SecuritySettings[Security Settings]
    
    style PrivacyDashboardPage fill:#f9f,stroke:#333,stroke-width:2px
```

### Homomorphic Encryption Page

Demonstrates privacy-preserving computation on encrypted data.

```mermaid
graph TD
    HomomorphicPage[Homomorphic Encryption Page] --> EncryptionStepper[Encryption Demo Stepper]
    
    EncryptionStepper --> EncryptStep[Encrypt Values]
    EncryptionStepper --> ComputeStep[Compute on Encrypted Data]
    EncryptionStepper --> DecryptStep[Decrypt Result]
    
    EncryptStep --> ValueInputs[Value Input Fields]
    EncryptStep --> EncryptButton[Encrypt Button]
    
    ComputeStep --> OperationSelector[Operation Selector]
    ComputeStep --> ComputeButton[Compute Button]
    
    DecryptStep --> DecryptButton[Decrypt Button]
    DecryptStep --> ResultDisplay[Result Display]
    
    style HomomorphicPage fill:#f9f,stroke:#333,stroke-width:2px
```

### Permissions Page

Manages third-party access to verification data.

```mermaid
graph TD
    PermissionsPage --> AccessControlSections[Access Control Sections]
    
    AccessControlSections --> CurrentAccess[Current Access Grants]
    AccessControlSections --> NewAccessForm[Grant New Access]
    AccessControlSections --> AccessHistory[Access History]
    
    CurrentAccess --> AccessList[Third-Party Access List]
    CurrentAccess --> RevokeButtons[Revoke Access Buttons]
    
    NewAccessForm --> ThirdPartySelector[Third-Party Selector]
    NewAccessForm --> DataTypeSelector[Data Type Selector]
    NewAccessForm --> ExpirySelector[Expiration Selector]
    
    AccessHistory --> AccessEvents[Access Events Timeline]
    
    style PermissionsPage fill:#f9f,stroke:#333,stroke-width:2px
```

### GDPR Requests Page

Handles GDPR-related user requests and compliance features.

```mermaid
graph TD
    GDPRPage[GDPR Requests Page] --> RequestSections[GDPR Request Sections]
    
    RequestSections --> NewRequest[New Request Form]
    RequestSections --> PendingRequests[Pending Requests]
    RequestSections --> CompletedRequests[Completed Requests]
    
    NewRequest --> RequestTypeSelector[Request Type Selector]
    NewRequest --> RequestDetails[Request Details Form]
    NewRequest --> SubmitButton[Submit Request Button]
    
    PendingRequests --> RequestStatus[Request Status Tracker]
    CompletedRequests --> DownloadButtons[Download Results Buttons]
    
    style GDPRPage fill:#f9f,stroke:#333,stroke-width:2px
```

## API Services

The frontend communicates with the backend through various service modules:

```mermaid
classDiagram
    class ApiBase {
        +axios instance
        +API_BASE_URL
        +request interceptors
    }
    
    class AuthService {
        +login(credentials)
        +register(userData)
        +logout()
    }
    
    class IdentityService {
        +verifyFace(userId, faceImage, userData)
        +verifyDocument(userId, documentImage, documentType, userData)
        +getVerificationStatus(userId, verificationType)
        +getVerificationHistory(userId)
        +getRiskAnalysis(userId)
    }
    
    class BlockchainService {
        +getVerificationAudit(userId)
        +generateZkp(userId, thirdPartyId, dataType, proofHash)
    }
    
    class PermissionService {
        +grantAccess(userId, thirdPartyId, dataTypes, expiryDays)
        +revokeAccess(userId, thirdPartyId)
        +getPermissions(userId)
    }
    
    class PrivacyService {
        +encryptValue(value)
        +computeOnEncryptedData(params)
        +decryptValue(encryptedValue)
    }
    
    class EncryptionService {
        +encryptData(userId, data, purpose)
        +decryptData(userId, encryptedData, keyId)
        +computeOnEncrypted(operation, encryptedValues)
    }
    
    class GdprService {
        +recordConsent(userId, purpose, dataCategories, thirdParties)
        +withdrawConsent(userId, consentId)
        +getUserConsents(userId)
        +checkConsent(userId, purpose, dataCategory)
        +submitDSR(userId, requestType, details)
        +getUserRequests(userId)
        +getDataAccessLogs(userId, limit)
        +generatePrivacyReport(userId)
        +anonymizeData(userId, data, sensitiveFields)
        +getRetentionPolicies()
    }
    
    ApiBase <|-- AuthService
    ApiBase <|-- IdentityService
    ApiBase <|-- BlockchainService
    ApiBase <|-- PermissionService
    ApiBase <|-- PrivacyService
    ApiBase <|-- EncryptionService
    ApiBase <|-- GdprService
```

## Context Providers

The application uses React Context API for state management:

```mermaid
classDiagram
    class AuthContext {
        +currentUser: Object
        +loading: Boolean
        +login(email, password)
        +logout()
    }
    
    class BlockchainContext {
        +connected: Boolean
        +account: String
        +loading: Boolean
        +error: String
        +connect()
        +disconnect()
    }
    
    class App {
        +AuthProvider
        +BlockchainProvider
    }
    
    class PageComponents {
        +useAuth()
        +useBlockchain()
    }
    
    App --> AuthContext : provides
    App --> BlockchainContext : provides
    PageComponents --> AuthContext : consumes
    PageComponents --> BlockchainContext : consumes
```

## User Flows

### Identity Verification Flow

```mermaid
sequenceDiagram
    participant User
    participant VerificationPage
    participant IdentityService
    participant BackendAPI
    
    User->>VerificationPage: Enter personal information
    User->>VerificationPage: Upload ID document
    VerificationPage->>IdentityService: verifyDocument(userId, document, type)
    IdentityService->>BackendAPI: POST /verification/document
    BackendAPI-->>IdentityService: Document verification result
    IdentityService-->>VerificationPage: Display verification status
    
    User->>VerificationPage: Upload facial image
    VerificationPage->>IdentityService: verifyFace(userId, faceImage)
    IdentityService->>BackendAPI: POST /verification/face
    BackendAPI-->>IdentityService: Facial verification result
    IdentityService-->>VerificationPage: Display verification status
    
    alt Verification successful
        VerificationPage-->>User: Show success message and blockchain receipt
    else Verification failed
        VerificationPage-->>User: Show failure message and retry options
    end
```

### Privacy Management Flow

```mermaid
sequenceDiagram
    participant User
    participant PrivacyDashboard
    participant GdprService
    participant BackendAPI
    
    User->>PrivacyDashboard: View privacy dashboard
    PrivacyDashboard->>GdprService: generatePrivacyReport(userId)
    GdprService->>BackendAPI: GET /privacy/report
    BackendAPI-->>GdprService: Privacy report data
    GdprService-->>PrivacyDashboard: Display privacy summary
    
    User->>PrivacyDashboard: Provide consent
    PrivacyDashboard->>GdprService: recordConsent(userId, purpose, dataCategories)
    GdprService->>BackendAPI: POST /privacy/consent
    BackendAPI-->>GdprService: Consent confirmation
    GdprService-->>PrivacyDashboard: Update consent list
    
    User->>PrivacyDashboard: Submit GDPR request
    PrivacyDashboard->>GdprService: submitDSR(userId, requestType, details)
    GdprService->>BackendAPI: POST /privacy/dsr
    BackendAPI-->>GdprService: Request confirmation
    GdprService-->>PrivacyDashboard: Update request status
```

### Homomorphic Encryption Demo Flow

```mermaid
sequenceDiagram
    participant User
    participant EncryptionDemo
    participant PrivacyService
    participant BackendAPI
    
    User->>EncryptionDemo: Enter values to encrypt
    EncryptionDemo->>PrivacyService: encryptValue(value)
    PrivacyService->>BackendAPI: POST /privacy/encrypt
    BackendAPI-->>PrivacyService: Encrypted value
    PrivacyService-->>EncryptionDemo: Display encrypted value
    
    User->>EncryptionDemo: Select operation
    EncryptionDemo->>PrivacyService: computeOnEncryptedData(params)
    PrivacyService->>BackendAPI: POST /privacy/compute
    BackendAPI-->>PrivacyService: Encrypted result
    PrivacyService-->>EncryptionDemo: Display encrypted result
    
    User->>EncryptionDemo: Request decryption
    EncryptionDemo->>PrivacyService: decryptValue(encryptedValue)
    PrivacyService->>BackendAPI: POST /privacy/decrypt
    BackendAPI-->>PrivacyService: Decrypted result
    PrivacyService-->>EncryptionDemo: Display final result
```

## User Interface

The frontend uses Material-UI components to create a consistent, responsive, and accessible user interface. The design follows a privacy-focused color scheme with indigo as the primary color and green as the secondary color.

### Theme Configuration

```mermaid
graph TD
    MaterialUITheme[Material-UI Theme] --> ColorPalette[Color Palette]
    MaterialUITheme --> Typography[Typography]
    MaterialUITheme --> Spacing[Spacing System]
    
    ColorPalette --> Primary[Primary: Indigo #3f51b5]
    ColorPalette --> Secondary[Secondary: Green #2e7d32]
    ColorPalette --> Background[Background: Light Gray #f5f5f5]
    
    Typography --> FontFamily["Font Family: 'Roboto', 'Helvetica', 'Arial', sans-serif"]
    Typography --> Headings[Hierarchical Headings]
    
    Spacing --> SpacingUnit[Spacing Unit: 8px]
    
    style MaterialUITheme fill:#f9f,stroke:#333,stroke-width:2px
```

## Responsive Design

The frontend is built with responsive design principles to provide an optimal user experience across different devices:

```mermaid
graph TD
    ResponsiveDesign[Responsive Design] --> GridSystem[Material-UI Grid System]
    ResponsiveDesign --> Breakpoints[Responsive Breakpoints]
    ResponsiveDesign --> FlexibleComponents[Flexible Components]
    
    GridSystem --> Container[Container Component]
    GridSystem --> Row[Row Structure]
    GridSystem --> Columns[Column Layout]
    
    Breakpoints --> Mobile[xs: Mobile - <600px]
    Breakpoints --> Tablet[sm: Tablet - ≥600px]
    Breakpoints --> Desktop[md: Desktop - ≥960px]
    Breakpoints --> LargeDesktop[lg: Large Desktop - ≥1280px]
    
    FlexibleComponents --> Cards[Responsive Cards]
    FlexibleComponents --> Forms[Adaptive Forms]
    FlexibleComponents --> Tables[Responsive Tables]
    
    style ResponsiveDesign fill:#f9f,stroke:#333,stroke-width:2px
```

## Deployment

The frontend can be deployed using Docker:

```mermaid
graph TD
    Docker[Docker Build] --> NodeImage[Node.js Base Image]
    NodeImage --> DependencyInstall[Install Dependencies]
    DependencyInstall --> BuildStep[Build React App]
    BuildStep --> NginxImage[Nginx Image]
    NginxImage --> StaticServing[Serve Static Files]
    
    style Docker fill:#bbf,stroke:#333,stroke-width:2px
    style NodeImage fill:#bfb,stroke:#333,stroke-width:2px
    style NginxImage fill:#fbf,stroke:#333,stroke-width:2px
```

## Code Structure

The codebase follows a modular organization:

```
frontend/
│
├── src/                    # Source files
│   ├── assets/             # Static assets
│   │   ├── Header.js       # Site header
│   │   └── Footer.js       # Site footer
│   │
│   ├── contexts/           # Context providers
│   │   ├── AuthContext.js  # Authentication context
│   │   └── BlockchainContext.js # Blockchain context
│   │
│   ├── pages/              # Page components
│   │   ├── HomePage.js     # Landing page
│   │   ├── VerificationPage.js # Identity verification
│   │   ├── ProfilePage.js  # User profile
│   │   ├── PermissionsPage.js  # Access permissions
│   │   ├── PrivacyDashboardPage.js # Privacy controls
│   │   ├── HomomorphicEncryptionPage.js # Encryption demo
│   │   └── GDPRRequestsPage.js # GDPR compliance
│   │
│   ├── services/           # API services
│   │   └── api.js          # API client configuration
│   │
│   ├── utils/              # Utility functions
│   ├── App.js              # Main App component
│   └── index.js            # Entry point
│
├── public/                 # Public assets
├── package.json            # Dependencies and scripts
└── Dockerfile              # Docker configuration
```

## Key Implementations

### Material-UI Integration

The application uses Material-UI extensively for UI components, ensuring a consistent and professional look and feel.

### Responsive Forms

Form components adapt to different screen sizes while maintaining usability and clear validation feedback.

### Progressive Disclosure

Complex verification processes are broken down into manageable steps using stepper components.

### Real-time Feedback

The UI provides immediate feedback for user actions through snackbar notifications and progress indicators.

### Accessibility

The application follows accessibility best practices including proper contrast ratios, keyboard navigation, and semantic HTML.

## Recommended Screenshot Placement

To enhance the documentation, it is recommended to add screenshots of the application in the following sections:

1. **Homepage Overview** - Add a screenshot of the landing page at the beginning of the document to provide a visual introduction.
2. **Verification Process** - Include screenshots of each step in the verification process in the Verification Page section.
3. **Privacy Dashboard** - Add screenshots of the dashboard tabs in the Privacy Dashboard Page section.
4. **Homomorphic Encryption Demo** - Include screenshots of the encryption demo steps in the Homomorphic Encryption Page section.
5. **GDPR Request Form** - Add a screenshot of the GDPR request form in the GDPR Requests Page section.
6. **Permissions Management** - Include screenshots of the permission control interface in the Permissions Page section.

For each screenshot, use the following format in the markdown file:

```
![Screenshot Description](path/to/screenshot.png)
*Caption explaining the feature shown in the screenshot*
```

## Conclusion

The frontend of the Privacy-Preserving Identity Verification System provides a comprehensive and user-friendly interface for secure identity verification and privacy management. By leveraging modern web technologies and design principles, it delivers a seamless experience while maintaining the highest standards of security and privacy. 