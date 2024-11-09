IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
               WHERE TABLE_NAME = 'Account' AND COLUMN_NAME = 'LastUpdated')
BEGIN
    ALTER TABLE Account ADD LastUpdated DATETIME;
END;

-- Check if the trigger already exists
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdateLastUpdated')
BEGIN
    EXEC('
    -- Create the trigger
    CREATE TRIGGER trg_UpdateLastUpdated
    ON Account
    AFTER INSERT, UPDATE
    AS
    BEGIN
        SET NOCOUNT ON;

        UPDATE Account
        SET LastUpdated = GETDATE()
        FROM Account a
        INNER JOIN inserted i ON a.AccountID = i.AccountID;
    END;
    ')
END;


-- Check if the trigger already exists
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_AccountInsert')
BEGIN
    EXEC('
    -- Create the trigger
    CREATE TRIGGER trg_AccountInsert
    ON Account
    AFTER INSERT
    AS
    BEGIN
        SET NOCOUNT ON;

        INSERT INTO AccountStats (AccountID)
        SELECT i.AccountID
        FROM inserted i;
    END;
    ')
END;