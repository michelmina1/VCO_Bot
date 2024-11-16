USE VCO;

-- Check if the current database version is less than 1.4
IF NOT EXISTS (SELECT * FROM DatabaseVersion WHERE VersionNumber >= '1.5')
BEGIN
    -- Create the AccountHistory table
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[AccountHistory]') AND type in (N'U'))
    BEGIN
        CREATE TABLE AccountHistory (
            HistoryID INT PRIMARY KEY IDENTITY(1,1),
            AccountID INT,
            Name NVARCHAR(100),
            Profession NVARCHAR(100),
            hwnd INT,
            threadID INT,
            ProcessID INT,
            WindowName NVARCHAR(255),
            WepDura INT,
            TotalLoad INT,
            CurrentLoad INT,
            x INT,
            y INT,
            Level INT,
            HP INT,
            SP INT,
            LastUpdated DATETIME,
            ChangeDate DATETIME DEFAULT GETDATE(),
            FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
        );
    END

    
-- Create a trigger to update the AccountHistory table when the Account table is updated
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE object_id = OBJECT_ID(N'[dbo].[trg_UpdateAccountHistory]'))
BEGIN
    EXEC('
    CREATE TRIGGER trg_UpdateAccountHistory
    ON Account
    AFTER UPDATE, INSERT
    AS
    BEGIN
        INSERT INTO AccountHistory (AccountID, Name, Profession, hwnd, threadID, ProcessID, WindowName, WepDura, TotalLoad, CurrentLoad, x, y, Level, HP, SP, LastUpdated)
        SELECT 
            i.AccountID, 
            i.Name, 
            i.Profession, 
            i.hwnd, 
            i.threadID, 
            i.ProcessID, 
            i.WindowName, 
            i.WepDura, 
            i.TotalLoad, 
            i.CurrentLoad, 
            i.x, 
            i.y, 
            i.Level, 
            i.HP, 
            i.SP, 
            GETDATE()
        FROM inserted i;
    END
    ');
END

    -- Update the database version to 1.4
    INSERT INTO DatabaseVersion (VersionNumber) VALUES ('1.5');
END
