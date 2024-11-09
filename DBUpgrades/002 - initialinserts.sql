IF NOT EXISTS (SELECT 1 FROM vco.dbo.config WHERE ConfigItem = 'Update')
BEGIN
    INSERT INTO vco.dbo.config (ConfigItem, Value) VALUES ('Update', 1);
END