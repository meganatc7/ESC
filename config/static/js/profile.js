const profileBtn = document.querySelector('#chg-profile')
const profileBox = document.querySelector('#profile-box')


profileBtn.addEventListener('click', ()=>{

  const changeForm = document.querySelector('#chg-form')
  const confirmBtn = document.querySelector('#confirm-btn')

  changeForm.classList.remove('not-visible')
  confirmBtn.classList.remove('not-visible')

  const input = document.querySelector('#id_profile')
  const csrf = document.getElementsByName('csrfmiddlewaretoken')

  input.addEventListener('change', ()=>{

    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)
    profileBox.innerHTML = `<img src="${url}" id="image" width="500px">`

    var $image = $('#image');

    $image.cropper({
      aspectRatio: 9 / 9,
      crop: function(event){

      }
    });

    var cropper = $image.data('cropper');

    confirmBtn.addEventListener('click', (event)=>{
      event.preventDefault()
      cropper.getCroppedCanvas().toBlob((blob)=>{
        console.log(blob)
        const fd = new FormData()
        
        fd.append('file', blob, 'change-profile.png')
        fd.append('csrfmiddlewaretoken', csrf[0].value)

        $.ajax({
          type: 'POST',
          url: '/accounts/update/profile/',
          data: fd,
          dataType: 'json',
          success: function(response){
            console.log('success')
            alert('success')
            window.location.href = ""
          },
          error: function(error){
            console.log(error)
          },
          cache: false,
          contentType: false,
          processData: false,
        })

      })
    })
  })
})

console.log('hi')
const wrote = document.querySelector('#wrote')
const liked = document.querySelector('#liked')
const commented = document.querySelector('#commented')
const article = document.querySelector('#all-article')
const likedArticle = document.querySelector('#liked-article')
const commentedArticle = document.querySelector('#commented-article')

wrote.addEventListener('click',()=>{
  wrote.className = 'nav-link activate'
  liked.className = 'nav-link'
  commented.className = 'nav-link'
  article.className = 'card-body'
  likedArticle.className = 'card-body not-visible'
  commentedArticle.className = 'card-body not-visible'
})

liked.addEventListener('click',()=>{
  wrote.className = 'nav-link'
  liked.className = 'nav-link activate'
  commented.className = 'nav-link'
  article.className = 'card-body not-visible'
  likedArticle.className = 'card-body'
  commentedArticle.className = 'card-body not-visible'
})

commented.addEventListener('click',()=>{
  wrote.className = 'nav-link'
  liked.className = 'nav-link'
  commented.className = 'nav-link activate'
  article.className = 'card-body not-visible'
  likedArticle.className = 'card-body not-visible'
  commentedArticle.className = 'card-body'
})