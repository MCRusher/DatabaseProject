CREATE TABLE Variants (
    variantID INTEGER PRIMARY KEY,--variantID is an alias for rowid (must be INTEGER and not INT), autoincrements if not specified
    variantName VARCHAR[30] NOT NULL UNIQUE,
    dateOfDiscovery DATE NOT NULL
);

CREATE TABLE Countries (
    countryID INTEGER PRIMARY KEY,
    countryName VARCHAR[40] NOT NULL UNIQUE,
    population INT NOT NULL,
    
    CHECK(population > 0)
);

CREATE TABLE VariantSpreadInCountries (
    variantID INT NOT NULL,
    countryID INT NOT NULL,
    vaccinated REAL,
    cases INT,
    deaths INT,
    
    FOREIGN KEY(variantID) REFERENCES Variants (variantID),
    FOREIGN KEY(countryID) REFERENCES Countries (countryID),
    PRIMARY KEY(variantID, countryID)
);