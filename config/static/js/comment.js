// 1. 모든 수정 버튼을 갖고온다.
const updateBtns = document.querySelectorAll('.commentUpdateBtn')
// ['1번 댓글 수정버튼', '2번 ...', '3번 ...', ...]

// 2. 모든 수정 버튼에 "클릭 이벤트를 단다."
updateBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    // 3. 기존의 내용을 지우고,
    document.querySelector(`#commentContent${btn.dataset.id}`).style.display = "none";
    // 4. 수정 form을 보여준다.
    document.querySelector(`#commentUpdateForm${btn.dataset.id}`).style.display = "block";
    // 수정, 수정 취소 토글
    document.querySelector(`#commentUpdate${btn.dataset.id}`).style.display = "none";
    document.querySelector(`#commentUpdateCancel${btn.dataset.id}`).style.display = "block";

  })
})

// 수정 취소 버튼
const updateCancelBtns = document.querySelectorAll('.commentUpdateCancelBtn')

updateCancelBtns.forEach(cancelBtn => {
  cancelBtn.addEventListener('click', () => {
    document.querySelector(`#commentUpdateForm${cancelBtn.dataset.id}`).style.display = "none";
    document.querySelector(`#commentContent${cancelBtn.dataset.id}`).style.display = "block";
    // 수정, 수정 취소 토글
    document.querySelector(`#commentUpdateCancel${cancelBtn.dataset.id}`).style.display = "none";
    document.querySelector(`#commentUpdate${cancelBtn.dataset.id}`).style.display = "block";
    
  })
})