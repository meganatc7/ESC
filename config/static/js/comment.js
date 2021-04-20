// 1. 모든 수정 버튼을 갖고온다.
const updateBtns = document.querySelectorAll('.commentUpdateBtn')
// ['1번 댓글 수정버튼', '2번 ...', '3번 ...', ...]

// 2. 모든 수정 버튼에 "클릭 이벤트를 단다."
updateBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    // 3. 기존의 내용을 지우고,
    console.log("success")
    console.log()
    console.log(document.getElementById("#commentContent{{ updateBtns.dataset.id }}"))
    // document.getElementById("#commentContent${updateBtns.dataset.id}").style.display = "none";
    // 4. 수정 form을 보여준다.
    
    // document.getElementById("#commentUpdateForm${updateBtns.dataset.id}").style.display = "block";
  })
})
// updateBtns.dataset.id == comment.id