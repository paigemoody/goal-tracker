$(function(){
            $('#edit-form').hide()
        });
        

        function updateGoals(evt, curUser) {
            // get all goal ids, make list of all ids that are checked 
            // make list of all ids that are not checked 
            const goalsStatus = {
                'userId': curUser,
                'goals' : {}
            }
             goalBoxes = document.getElementsByClassName('goal-completeness-check') 
            // look at all goals, if associated input box is clicked add completed
            // data to goalStatus
            for (i = 0; i < goalBoxes.length; i++) {
                    // get the value of the goal's checkbox
                    const goalBox = goalBoxes[i];
                    const goalId = goalBox.id;
                    const goalBoxStatus = goalBox.checked;
                    
                    goalsStatus.goals[goalId] = {}
                    goalsStatus.goals[goalId]['complete'] = goalBoxStatus;
                    
                };

            goalsStatus.goals = JSON.stringify(goalsStatus.goals)
            $.post('/save_goals', goalsStatus, confirmUpdateGoals);
        }
        
        // alert user that changes have been saved
        function confirmUpdateGoals(confMessage) {
            alert(confMessage);
        };

        // add new goal when add button is clicked 
        $('#add-goal-button').on('click', function(){

            const newGoalTitle = $('#new-goal-title').val();
            const newGoalNotes = $('#new-goal-notes').val();

            if ((newGoalNotes.length + newGoalTitle.length) > 2){
                const goalData = {
                title : newGoalTitle,
                notes : newGoalNotes
                }
                $.post('/add_goal', goalData, confirmAddGoal);

            } 

            else {
                alert('Input too short.')
            }
            
        })

        // alert user that changes have been saved
        function confirmAddGoal(confMessage) {
            alert(confMessage);
            location.reload();

        };


        // delete goal when associated button is clicked
        function deleteGoal(evt, goalId) {

            goalInfo = { id : goalId }
            $.post('/delete_goal', goalInfo, confirmDeleteGoal);
        }

        function confirmDeleteGoal(confMessage) {
            alert(confMessage);
            location.reload();
        };


        // change goal to text boxes on click of button

        function editGoal(evt, goalId) {

            $('#edit-form').show();

            goalTitle = document.getElementById(goalId).getElementsByClassName("goal-title")[0].innerText;
            goalNotes = document.getElementById(goalId).getElementsByClassName("goal-notes")[0].innerText;
            
            $('#new-title').val(goalTitle);
            $('#new-notes').val(goalNotes);
            $('#goal_id').val(goalId);
        };

        $('#cancel').on('click', function(){$('#edit-form').hide()})

        $('#save-edit').on('click', function(){
            // when edit is saved send goalid, new title and new notes to backend to be updated
        
            updates = {
                goalId : $('#goal_id').val(),
                newTitle :  $('#new-title').val(),
                newNotes : $('#new-notes').val()
            };

            $.post('/edit_goal', updates, confirmEdits);

        })

        function confirmEdits(confMessage){
            alert(confMessage);
            location.reload();
        }