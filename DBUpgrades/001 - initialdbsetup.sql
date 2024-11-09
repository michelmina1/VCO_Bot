USE VCO;
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND type in (N'U'))
BEGIN
    CREATE TABLE Account (
        AccountID INT PRIMARY KEY IDENTITY(1,1),
        Name NVARCHAR(100) NOT NULL,
        Profession NVARCHAR(100) NOT NULL
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Status]') AND type in (N'U'))
BEGIN
    CREATE TABLE Status (
        StatusID INT PRIMARY KEY IDENTITY(1,1),
        StatusName NVARCHAR(100) NOT NULL
    );
END
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Config]') AND type in (N'U'))
BEGIN
    CREATE TABLE Config (
        ConfigItem NVARCHAR(100) PRIMARY KEY,
        Value INT NOT NULL
    );
END
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[AccountStatus]') AND type in (N'U'))
BEGIN
    CREATE TABLE DatabaseVersion (
        VersionID INT PRIMARY KEY IDENTITY(1,1),
        VersionNumber NVARCHAR(10) NOT NULL,
        AppliedDate DATETIME NOT NULL DEFAULT GETDATE()
    );

    INSERT INTO DatabaseVersion (VersionNumber) VALUES ('1.0');

    CREATE TABLE AccountStatus (
        AccountID INT,
        StatusID INT,
        PRIMARY KEY (AccountID, StatusID),
        FOREIGN KEY (AccountID) REFERENCES Account(AccountID),
        FOREIGN KEY (StatusID) REFERENCES Status(StatusID)
    );
END
ELSE
BEGIN
    ALTER TABLE AccountStatus
    ADD FOREIGN KEY (AccountID) REFERENCES Account(AccountID),
        FOREIGN KEY (StatusID) REFERENCES Status(StatusID);
END

-- AccountStats Table
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[AccountStats]') AND type in (N'U'))
BEGIN
    CREATE TABLE AccountStats (
        AccountID INT PRIMARY KEY,
        WepDura INT,
        TotalLoad INT,
        CurrentLoad INT,
        x INT,
        y INT,
        Level INT,
        HP INT,
        SP INT,
        FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[AccountSkills]') AND type in (N'U'))
BEGIN
    CREATE TABLE AccountSkills (
        AccountID INT PRIMARY KEY,
        Voyage INT,
        SeaBattle INT,
        FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ShipStatus]') AND type in (N'U'))
BEGIN
    CREATE TABLE ShipStatus (
        ShipLvl INT,
        TotalLoad INT,
        CurrentLoad INT,
        Provisions INT,
        CannonsLeft INT,
        CannonsRight INT
    );
END
