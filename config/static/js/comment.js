const commentUpdeat = (id) => {
  let commentUpdate = document.querySelector(`.commentUpdate${id}`);
  let commentUpdateForm = document.querySelector(`.commentUpdateForm${id}`);
  let commentContent = document.querySelector(`.commentContent${id}`);
}

$(document).ready(function(){
  $("#commentUpdate").click(function(){
    $("#commentUpdateForm").toggle();
    $("#commentContent").toggle();
  });
  $("#comment_update_cancel").click(function(){
    $("#comment_content").show();
    $("#comment_update_form").hide();
  });
});