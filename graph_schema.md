# Compliance Knowledge Graph Schema

## Node Types

### Regulation

Represents a regulation source.

Example:

* GDPR

### Article

Represents a GDPR article.

Examples:

* Article 5
* Article 6
* Article 17
* Article 25
* Article 28
* Article 32
* Article 44

Properties:

* article_number
* title
* risk_level
* jurisdiction

### Policy

Represents internal company policies.

Examples:

* Employee Data Policy
* Customer Privacy Policy
* Vendor Management Policy

Properties:

* name
* department

### Procedure

Represents operational procedures.

Examples:

* Data Deletion Procedure

Properties:

* name
* owner

---

## Relationships

### HAS_ARTICLE

Regulation → Article

Example:

GDPR → Article 17

### IMPLEMENTED_BY

Article → Policy

Example:

Article 17 → Customer Privacy Policy

### REFERENCES

Policy → Procedure

Example:

Customer Privacy Policy → Data Deletion Procedure

### SUPPORTS_COMPLIANCE

Procedure → Article

Example:

Data Deletion Procedure → Article 17
