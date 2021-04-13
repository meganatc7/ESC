const profileBtn = document.querySelector('#chg-profile')

profileBtn.addEventListener('click', ()=>{

  const changeForm = document.querySelector('#chg-form')
  const confirmBtn = document.querySelector('#confirm-btn')

  changeForm.classList.remove('not-visible')
  confirmBtn.classList.remove('not-visible')

  const input = document.querySelector('#id_file')
  const imageBox = document.querySelector('#image-box')

  input.addEventListener('change', ()=>{
    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)
    imageBox.innerHTML = `<img src="${url}" id="image" width="500px">`
  })
})
