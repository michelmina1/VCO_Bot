IF NOT EXISTS (SELECT * FROM DatabaseVersion WHERE VersionNumber >= '1.1')
BEGIN
IF NOT EXISTS (SELECT 1 FROM vco.dbo.config WHERE ConfigItem = 'Update')
BEGIN
    INSERT INTO vco.dbo.config (ConfigItem, Value) VALUES ('Update', 1);
END
INSERT INTO DatabaseVersion (VersionNumber) VALUES ('1.1');
END