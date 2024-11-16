USE VCO;

-- Check if the current database version is less than 1.3
IF EXISTS (SELECT * FROM DatabaseVersion WHERE VersionNumber < '1.3')
BEGIN
    -- Add columns to Account table if they do not exist
    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND name = 'WepDura')
    BEGIN
        ALTER TABLE Account ADD WepDura INT;
    END

    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND name = 'TotalLoad')
    BEGIN
        ALTER TABLE Account ADD TotalLoad INT;
    END

    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND name = 'CurrentLoad')
    BEGIN
        ALTER TABLE Account ADD CurrentLoad INT;
    END

    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND name = 'x')
    BEGIN
        ALTER TABLE Account ADD x INT;
    END

    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND name = 'y')
    BEGIN
        ALTER TABLE Account ADD y INT;
    END

    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND name = 'Level')
    BEGIN
        ALTER TABLE Account ADD Level INT;
    END

    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND name = 'HP')
    BEGIN
        ALTER TABLE Account ADD HP INT;
    END

    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[Account]') AND name = 'SP')
    BEGIN
        ALTER TABLE Account ADD SP INT;
    END

    -- Drop AccountStats table
    DROP TABLE AccountStats;
    DROP TRIGGER [dbo].[trg_AccountInsert]

    -- Update the database version to 1.3
    INSERT INTO DatabaseVersion (VersionNumber) VALUES ('1.3');
END
