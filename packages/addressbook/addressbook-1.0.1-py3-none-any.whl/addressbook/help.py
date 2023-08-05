help_content = '''
HELP & DOCUMENTATION
-----------------------------------------------------------------------------------------------------------

Changes To This Release: Changes section at bottom of help.

This application is a database-based application that has four basic actions.
  1. Add record
  2. View record
  3. Update record
  4. Delete record

Each of the four above actions applies to the following sections.
  1. People
     a. Search for person
  2. Contacts (email and phone)
  3. Addresses
  4. Identification
  5. Relationships
     a. Search for person
  6. Comments

Glossary

  7. Glossary & Field Definitions

Search

  8. Search Functions


Section 1: Person
-----------------------------------------------------------------------------------------------------------

ADD

  All address book entries start with adding a person record. No other records, such as
  phone, email, or addresses may be entered until a person is first entered.

  1. Add person record by clicking the "New" from the menu and selecting "Person Record"
  2. First and last name are required, so enter both.
  3. Enter any remaining data for the remaining fields if needed.
     a.  Dates use YYYY-MM-DD format where "-" is a "dash" between the date parts.
     b.  Dates must be complete, if entered because partial dates will be rejected.
  4. Click the "Save" button.

VIEW

  1. Select a person record from the list of people.
  2. To see additional information click the tab for the corresponding information you wish to see.
     a. If all other tabs contain no information then use the menu to add the additional information.
  3. If no people are listed you may need to enter a person first, or remove any search filters.
  4. Alternatively, you can search for a person. (Assumes 1 or more people are entered)
     a. Select a filter
     b. Pick how the value will be searched by clicking "Contains" or "Equals"
        The "Contains" option searches for selected filters which contain the specified value.
     c. Click the "Search" button.
     d. Note: To "clear" a filter select "All" from the filter list and click the "Search" button.
        All is the default filter.

UPDATE

  1. You cannot update a person record until one has been created.
  2. Create a person record if it does not exist.
  3. Select the row for the person you wish to edit.
  4. Change the data in the fields on the "Person" tab as desired
  5. Click the "Save Changes" button (long bar at the bottom of the window)
     a. Note: if the other tabs include changes all changes will be saved.
        No need to click save after every edit. This applies only to the
        data entry fields on the main tabs. Person, Address, Identification, Relationships,
        and Comments.  All other edits are done in different windows.


DELETE

WARNING: The "Delete Person" button removes all information! To repeat, ALL INFORMATION for the
selected person and CANNOT be undone.

  1. Select a person to delete.
  2. Click the "Delete Person" button on the "Person" tab.
     a. If no people are listed then it is possible you need to clear the search filters.
     b. If search filters are not applied and no people are listed then none are entered to delete.


Section 2: Contacts
-----------------------------------------------------------------------------------------------------------

ADD

  1. Select a person.
  2. Click the menu "Selected Person"
  3. Click "Add Email" or "Add Phone" menu item.
  4. Phone
     a. Enter area code, exchange, and trunk
     b. Enter a sequence number
     c. Select a contact type (phone type)
     d. Click "Save" button
  5. Email
     a. Enter email address
     b. Enter sequence number
     c. Select contact type (email type)
     d. Click "Save" button.

VIEW

  1. Select a person
  2. Phone and email contacts appear in the lists, if any on the "Person" tab.
     If no phone or email is showing, follow the directions for adding above.


UPDATE

  1. Select a person.
  2. Select a contact (phone or email).
  3. Click the corresponding "Edit Phone" or "Edit Email" button.
  4. Phone
     a. Change the area code, exchange, and trunk as expected.
     b. Change the sequence number as expected.
     c. Change the type as expected.
     d. Click "Save" button.
  5. Email
     a. Change email address as expected.
     b. Change sequence number as expected.
     c. Change type as expected.
     d. Click "Save" button.

  Note: Sequence numbers are flexible and can be any number and do not need to follow any
  specific increment. There is no automatic re-ordering of sequence number and therefore
  you will need to edit each contact in the list to reorder the sequence. The first number
  in the sequence is considered the "Main" contact and will always be selected by default
  when displaying the contacts lists.

DELETE

  1. Select a person.
  2. Select a contact (phone or email).
  3. Click the corresponding delete button ("Delete Phone" or "Delete Email").


Section 3: Address
-----------------------------------------------------------------------------------------------------------

ADD

  1. Select a person.
  2. Click "Selected Person" menu.
  3. Select "Add Address" from the menu.
  4. Enter required fields.
     a. Address Line 1
     b. City
     c. State
     d. Zip Code
     e. Address Type
     f. Sequence Number
  5. Enter other fields as necessary.
  6. Click "Save Button".

VIEW

  1. Select a person.
  2. Click the "Address Tab".
  3. Select an address from the list if one is not already selected.

UPDATE

  1. Select a person.
  2. Click the "Address Tab".
  3. Select an address from the list
  4. Edit the address fields as required
     a. Note: Required fields are the same as for ADD above.
  5. Click the "Save Changes" button.

DELETE

  1. Select a person.
  2. Select the "Address Tab" if not already selected.
  3. Select address from the list.
  4. Click the "Delete Address" button.


Section 4: Identification
-----------------------------------------------------------------------------------------------------------

  The identification section is useful for tracking information about issued identification cards, such as
  drivers licenses and other governmentally issued identification documents.  If tracking of
  identification is not useful from a documentation point of view it may be useful to help distinguish
  between people with the same names.  For example, when two people exist with the same first and last name
  you may want to use the "ID Number" field to simply distinguish between the two people.

ADD

  1. Select a person.
  2. Click the "Selected Person" menu.
  3. Select the "Add Identity" from the menu.
  4. Enter required fields.
     a. ID number
     b. Type
     c. No other fields are required.
  5. Enter data for remaining fields.
     a. Note: The "record location" field may contain any data however, the original idea for this field
        was to contain the file path for where a digital copy of the identity was stored on your computer.
        For example, a scanned image of a drivers license in your documents folder.
  6. Click the "Save" button.

VIEW

  1. Select a person.
  2. Click the "Identification tab" if not already selected.
  3. Select a identification row from the list.

UPDATE

  1. Select a person.
  2. Click the "Identification tab" if not already selected.
  3. Select a identification row from the list.
  4. Edit fields as necessary.
  5. Click the "Save Changes" button.

DELETE

  1. Select a person.
  2. Click the "Identification tab" if not already selected.
  3. Select a identification row from the list.
  4. Click the "Delete Identification" button.


Section 5: Relationships
-----------------------------------------------------------------------------------------------------------

  The relationships section is for assigning relationships between people. You do not need to assign
  reciprocal relationships as this is done automatically.  For example, if you assign a person
  as a parent then a child relationship is created as well. This means two relationships are created; one
  as the parent and one as the child for each respective person in the relationship.

  The majority of the relationship types are self explanatory. However, special mention is made here
  for the term NIBLINGS. In the English language my research seems to indicate there is not a word,
  a collective noun, for your nieces and nephews as a collective term.  So, here, NIBLING is used
  to mean the relationship is that of niece or nephew to an aunt or uncle. Gender is intentionally
  omitted here to keep the relationship assignments simple.

  Generally, a simple list of related people and not intended as a "family tree" feature.

ADD

  1. Select a person.
  2. Click the "Selected Person" menu.
  3. Select the "Add Relationship" menu item.
  4. Select a related person from the list or search for a related person.
     a. Note: Search for people functions the same as search for person on the main window.
  5. Select a relationship type from the options menu (next to the save button).
  6. Click the "Save" button.

VIEW

  1. Select a person from the list.
  2. Click the "Relationships" tab.

UPDATE

  There is NO UPDATE FEATURE due to the complexity of possible relationship assignments.
  To correct an invalid relationship do the following.

  1. Select a person
  2. Select the "Relationships tab".
  3. Select the invalid ( or incorrect ) relationship.
  4. Click the "Delete Relation" button.
  5. Follow the steps for ADD relationship.
     a. Generally, the whole process for fixing a relationship is "delete and add".

DELTE

  1. Select a person
  2. Select the "Relationships tab".
  3. Select the unwanted relationship.
  4. Click the "Delete Relation" button.
     a. "Delete Relation" DOES NOT DELETE THE PERSON only the relationship.


Section 6: Comments
-----------------------------------------------------------------------------------------------------------

  The comments section is for any information you wish to capture that is not already available in another
  section.  For example, a person is only available for contact during certain hours of the day, so you may
  want to make a comment reminding you of the best time to call.

  As with any data that is entered free-form and without structure; it is up to the user to make entries
  in an organized what that promotes ease of use and makes sense. The comments section does not
  impose any structure.

ADD

  There is NO SPECIFIC ADD FUNCTION for comments. ADD is handled automatically through the UPDATE
  process when no previous comments exit. Generally, new comments are added on-the-fly.

  Simply do the following to capture a comment.

  1. Select a person.
  2. Click the "Comments" tab.
  3. Enter a comment in the comment area.
  4. Click the "Save Changes" button.

VIEW

  1. Select a person.
  2. Click the "Comments" tab.

UPDATE

  1. Select a person.
  2. Click the "Comments" tab.
  3. Change or add to the comments as necessary.
  4. Click the "Save Changes" button.

DELETE

  There is NO SPECIFIC DELETE FUNCTION for comments. This is handled through the UPDATE process.
  Do the following to delete comments.

  1. Select a person
  2. Select the "Comments" tab.
  3. Use the mouse to select unwanted comments.
  4. Use the "DELETE-KEY" on your keyboard to delete.
  5. Click the "Save Changes" button.


Section 7: Glossary & Field Definitions
-----------------------------------------------------------------------------------------------------------

  The majority of terms and fields in a simple address book are generally understood, therefore, we will
  only list a few items here that may need clarification.

  Phone Numbers:
     In the U.S.A. a phone number consists of an area code, an exchange, and a trunk consisting a set of
     numbers in the following pattern. XXX-XXX-XXXX. Prefixes such as 1+ phone number are excluded
     in this application and assumed to be common knowledge and the user will use the correct prefix for
     a phone number. Assumptive, we know, so maybe a feature in the future.

     Non-U.S.A phone numbers are excluded in this application at the current time and may be
     a future feature.  To capture foreign phone numbers please use the comments section for now.

  Sequence Number:
     Sequence numbers are used through the application in different sections.  A sequence number is
     simply a way to order the information in ways that are meaningful to the user.
     For example: Consider setting the most important phone number, or primary phone number, you would
     call first; as sequence number one (1).

  Postal Code ( Addresses ):
     Postal code is intended for any code not meeting the United States Postal Mail Service address
     regulations that is necessary for a mailing address to non- USA destinations.  For example,
     Canada does not use a "zip-code" but a postal code instead.

  ID Number ( Identification ):
     The number or alpha numeric identifier printed on an identification document which is used
     as the identifier for the document. For example, a drivers license has a drivers license number
     which would be entered into the ID No. field.

  Issuing Authority ( Identification ):
     The governing body which authorizes the publication or production of identification documentation.
     For example a state in USA, such as Pennsylvania, would be the issuing authority for drivers license.

  Issuing Entity ( Identification ):
     Not to be confused with "Issuing Authority", the issuing entity is the governmental agent responsible
     for the actual issuance of identification. For example, the state of Pennsylvania is the issuing
     authority but the Pennsylvania Department of Transportation ( PA DOT ) is the issuing entity.

  Identification Type ( Identification ):
     The list presented in the application for type is generally the USA federally accepted identification
     documents permitted and expected by various federal and state agencies. This is not a comprehensive
     list but you should get the idea.

  Nibling ( Relationships ):
     A term to collectively represent nieces and nephews.  When NIBLING is selected as a relationship
     type this means the related persons are that of niece or nephew to aunt or uncle.  This is is
     an arbitrary term.  The term Nibling is derived from "Sibling" replacing "S" with "N" to
     represent (N)ieces and (N)ephews. For users interested in more about this Google the term
     "collective noun" and you will find many examples where the English language lacks collective nouns.

  Parent Sibling ( Relationships ):
     Parent sibling is the reciprocal of Nibling.  When Nibling is selected the related person is
     assigned the reciprocal relationship of "Parent Sibling".  To clarify, an aunt or uncle is
     the sibling to the parent of a niece or nephew. Like nibling, there is no collective term for
     aunts and uncles in the English language. (as far as we know).

  Reciprocal ( Relationships ):
     This is not a term used directly in the application but requires some mention here.
     For all relationship assignment it is assumed that a reciprocal relationship should be
     created. For example, if assigning a related person as a child to the specified person then
     it is assumed the specified person is the parent of the child. In other words, a child added
     as a relation automatically assigns the parent. Therefore, selecting the parent in the people list
     will show a list of children or selecting a child from the people list will list the parents.

  Delete Person ( Person Tab ):
     The delete person button completely removes ALL information for a person and cannot be undone.
     This means ALL information; contacts, addresses, identification, relationships, and comments.


Section 8: Search Functionality
-----------------------------------------------------------------------------------------------------------

  Search functionality is provided on the main window and the relationship window and consists
  of the following:

    1. Search Filter
    2. Search term (text box for input)
    3. Search Type
       a. Contains
       b. Equals

  To search for a person do the following:
    1. Select a search filter.
    2. Select a search type.
    3. Enter a search term which corresponds to the search filter.
       For example, when you pick city as a filter you enter the
       name of a city not a name of a person.
    4. Click the search button.

    NOTE: Search terms, are case "insensitive", capitalization is not considered in search results.

  Search Types

    Contains        - Search term is contained within search filter.
                      For example: Find all people which last name contains "on"
                      The results would be any matches for johnson, wilson, hilton, jones.
                      The search term "on" may appear anywhere in the last name.

    Equals          - Search term is a full-match and equals the search filter.
                      For example: Find all people with the last name "jones".
                      The search will only return people who's last name is "jones" and nothing else.

    Note:             When using search types the "Contains" type is more dynamic but you may not
                      always get the results you want. The more characters you enter the more
                      precise the search gets. For example, if you search by for first names that
                      contains "im" you will get Jim, Tim, Timmy, Ginny, etc.. However, in this
                      example, if you search for "Gin" you will only get "Ginny" as a result.
                      The extra "G" in the search term narrows the results.


  Search Filters

    Select Filter   - Nothing is selected, search will not be performed.
    First Name      - Search for people by first name.
    Last Name       - Search for people by last name.
    Address Line 1  - Search for people at address line 1.
    Address Line 2  - Search for people at address line 2.
    City            - Search for people in the city.
    State           - Search for people in the state.
    Zip Code        - Search for people is a zip code.
    Phone           - Search for people by phone number.
    Email           - Search for people by email.
    Identification  - Search for people by Identification Number.
    All             - Don't search just return all people in the database.

CHANGES

Changes in this release: [1.0.1]
Added sorting to grids for main dashboard and relationships.
	Table headers sort by clicked column header.
Added postal code and status to address tab on dashboard to match address entry window.
Added settings for default window sizes so users can adjust, if needed, for their operating system.
	Change defaults by editing settings.py file.
Allow users to change the default search LIMIT on rows returned for search.
	Change defaults by editing settings.py file.

'''