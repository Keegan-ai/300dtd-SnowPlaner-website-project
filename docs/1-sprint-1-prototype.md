# Sprint 1 - A Working UI Prototype


## Sprint Goals

Develop a prototype that simulates the key functionality of the system, then test and refine it so that it can serve as the model for the next phase of development in Sprint 2.

[Figma](https://www.figma.com/) is used to develop the prototype.


---

## Initial Database Design

Replace this text with notes regarding the DB design.

![SCREENSHOT OF DB DESIGN](screenshots/improved_DB.png)



### Required Data Input

1. Most data will come from a web app where users enter it manually.
2. When signing up, users will give their name, username, and password, which will be saved in the users table with the password stored securely in a hashed form.
3. Users can create groups by giving them a name and optionally adding members.
4. When a user joins a group, their user_id will be linked to the group_id in the membership table.
5. To add a task, users will enter the task name, date and time, and optional details like a maprunner_url and description, and mark if the task is complete.
6. Each task will be linked to a specific group and/or user.

### Required Data Output

1. The system will show user profiles with their username, name, and groups they belong to.
2. Each group will show its name, members, and linked tasks.
3. Tasks will list the name, date and time, description, completion status, and a maprunner_url link if available.
4. Reports will compare completed and pending tasks for each user or group.
5. Users can filter tasks by completion status, group, or date range.

### Required Data Processing

1. The system will join the users, membership, group, and tasks tables to combine related data.
2. Tasks can be filtered and sorted by date, completion status, or group.
3. User passwords will be hashed during registration for security.
4. The system will check that data is in the right format, such as valid timestamps and URLs.
5. Reports will total how many tasks are completed per group and how many are assigned to each user.
6. Optional fields like maprunner_url and description will only be used if they are provided.


---

## UI 'Flow'

The first stage of prototyping was to explore how the UI might 'flow' between states, based on the required functionality.

This Figma demo shows the initial design for the UI 'flow':

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="1440" height="1024" src="https://embed.figma.com/proto/nHkOgxPdsQ0wW41REtSelK/Web-Design?node-id=68-93&p=f&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=68%3A93&show-proto-sidebar=1&embed-host=share" allowfullscreen></iframe>

### Testing

The way i tested this first ui prototype was making other's experience it like how it would work. I am going to use their feedback to make improvements to my design. Ill put the notes here as evident on what my user had said:
User Feedback:
1. Change "logged in" to not be a button
2. Add "Sign out/Log out" button 
3. Add A register page where users can create an account before they log in ( via login page). This is better for managing
multiple accounts one user may have
4. Display Group join code at the top of the screen "Group Info" page.
5. Add a filter to the URL box to nly allow maprunner URLs
6. "Leave Group" Button should have a confirmation message that requires the group code to proceed( as safety measure )
7. Change layout so that the important stuff stay fixed on the screen.
8. Change the create to sign up 
9. Make it so that when you  log out it takes you to the welcome page and change the sign up button to go to sign in page 

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.
I changed the design and how it would work. 
Here are the changes made:
1. I changed the logged in button to be a sign out/Log out button 
2.  I added a sign in page and added a create a account page
3. I added round buttons that would be stuck and not move from the screen to make it more accesible.
4. I changed it so that you need to use the group code to leave the group and i added the group code to where you will see the hole group
5. I changed the url to only accept maprunner urls.
6. Changed on how my flow actually goes like my sign up button now goes to the sign in page and the log out button goes to the welcome 
7. Also changed some wording in the sign up page 

Here: is my updated prototype:

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="1440" height="1024" src="https://embed.figma.com/proto/nHkOgxPdsQ0wW41REtSelK/Web-Design?node-id=104-135&p=f&scaling=min-zoom&content-scaling=fixed&page-id=104%3A24&starting-point-node-id=104%3A135&embed-host=share" allowfullscreen></iframe>

### Further Testing

Sharing this again with my end-users. They seemed to like my flow because it was easy to navigate without problem.
Meaning my end-users were satisfied so im confident that i can move on to the initial prototype
---

## Initial UI Prototype

The next stage of prototyping was to develop the layout for each screen of the UI.

This Figma demo shows the initial layout design for the UI:

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="1440" height="1024" src="https://embed.figma.com/proto/nHkOgxPdsQ0wW41REtSelK/Web-Design?node-id=148-117&p=f&scaling=min-zoom&content-scaling=fixed&page-id=131%3A151&starting-point-node-id=148%3A117&embed-host=share" allowfullscreen></iframe>

### Testing
I showed my roughed out design for my website to my end-users and i wanted them to give feedback on the usability of the system and also the system functionality

Here is there feedback:
 1. Change order of login pages
 2. "create group" button and "join group" button should scroll with the user 

### Changes / Improvements

1. I've switched around the sign up page to now go to the sign in page
2. Both "create a group" and "join group" buttons now stay fixed to the home page
3. Added the abilitie so that users can create their own passcode for their group

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="1440" height="1024" src="https://embed.figma.com/proto/nHkOgxPdsQ0wW41REtSelK/Web-Design?node-id=197-208&p=f&scaling=min-zoom&content-scaling=fixed&page-id=197%3A3&starting-point-node-id=197%3A208&embed-host=share" allowfullscreen></iframe>

After showing my end-users again. They seemed to like the functionality because it was easy to use and looks nice. So i can continue without worry.
---

## Refined UI Prototype

Having established the layout of the UI screens, the prototype was refined visually, in terms of colour, fonts, etc.

This Figma demo shows the UI with refinements applied:

*FIGMA REFINED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*

### Testing

Replace this text with notes about what you did to test the UI flow and the outcome of the testing.

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

*FIGMA IMPROVED REFINED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*


---

## Sprint Review

Replace this text with a statement about how the sprint has moved the project forward - key success point, any things that didn't go so well, etc.

