Feature: import feeds from opml file
  A management command allows to import an opeml file (for a specified user)

  Scenario: Import an valid opml file and a user
    Given a opml file contining a feed in one subcategory
    When the file is imported
    Then there exists a feedobject for this feed
    And a userfeed object
    And a categoryobject in the database