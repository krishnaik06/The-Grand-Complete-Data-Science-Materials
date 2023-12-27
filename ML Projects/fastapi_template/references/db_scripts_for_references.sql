/****** Object:  Table [dbo].[APIConsumers]    Script Date: 9/19/2023 1:09:52 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[APIConsumers](
	[consumer_id] [int] IDENTITY(1,1) NOT NULL,
	[user_name] [nvarchar](50) NULL,
	[full_name] [nvarchar](50) NULL,
	[email] [nvarchar](50) NULL,
	[hashed_password] [nvarchar](200) NULL,
	[disabled] [bit] NULL,
 CONSTRAINT [PK_APIConsumers] PRIMARY KEY CLUSTERED 
(
	[consumer_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ExceptionLog]    Script Date: 9/19/2023 1:09:52 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ExceptionLog](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[logged] [datetime] NULL,
	[level] [nvarchar](200) NULL,
	[message] [nvarchar](max) NULL,
	[logger] [nvarchar](500) NULL,
 CONSTRAINT [PK_ExceptionLog] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[APIConsumers] ADD  CONSTRAINT [DF_APIConsumers_disabled]  DEFAULT ((0)) FOR [disabled]
GO
/****** Object:  StoredProcedure [dbo].[exception_log]    Script Date: 9/19/2023 1:09:52 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[exception_log]
(
@logged DATETIME,
@level NVARCHAR(50),
@message NVARCHAR(MAX),
@logger NVARCHAR(500)
)
AS
BEGIN
	
	INSERT INTO [dbo].[ExceptionLog](
				[logged]
				,[level]
				,[message]
				,[logger]
				)
	SELECT @logged
			,@level
			,@message
			,@logged
END
GO
/****** Object:  StoredProcedure [dbo].[getAPIConsumerDetails]    Script Date: 9/19/2023 1:09:52 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- EXEC getAPIConsumerDetails 'johndoe'
-- =============================================
CREATE PROCEDURE [dbo].[getAPIConsumerDetails] 
(
@user_name NVARCHAR(50)
)
AS
BEGIN
	SELECT * FROM [dbo].[APIConsumers]
	WHERE user_name = @user_name
END
GO
USE [master]
GO
ALTER DATABASE [MusaddiqueHussainLabs] SET  READ_WRITE 
GO
