// 필요한 각각의 태그들을 변수화
const imageBox = document.querySelector('#image-box')
const input = document.querySelector('#id_image')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const confirmBtn = document.querySelector('#confirm-btn')


// input변수에 이벤트
input.addEventListener('change', ()=>{

  confirmBtn.classList.remove('not-visible')

  //file 정보를 가져와서 img_data 변수에 저장
  const img_data = input.files[0]
  // Blob 객체를 나타내는 URL을 포함한 DOMString 생성
  const url = URL.createObjectURL(img_data)
  // 가져온 url로 imageBox에 고른 이미지 띄우기
  imageBox.innerHTML = `<img src="${url}" id="image" width="500px">`

  // jQuery로 이미지 태그 가져오기
  var $image = $('#image');

  // 이미지 크롭 기능
  $image.cropper({
    aspectRatio: 9 / 9,
    crop: function(event) {

    }
  });

  var cropper = $image.data('cropper');

  confirmBtn.addEventListener('click', (event)=>{
    event.preventDefault()
    cropper.getCroppedCanvas().toBlob((blob)=>{
      console.log(blob)
      const fd = new FormData()
      const b_url = URL.createObjectURL(blob)

      fd.append('file', blob, 'my-image.png')
      fd.append('csrfmiddlewaretoken', csrf[0].value)
      fd.append('url', b_url)
      

      $.ajax({
        type: 'POST',
        url: '/accounts/cropped/',
        // url: '{% url "accounts:cropped" %}',
        enctype: 'multipart/form-data',
        data: fd,
        dataType: 'json',
        success: function(response){
          console.log(response)
          console.log(response.path)
          const hiddenInput = document.querySelector('#hidden-input')
          hiddenInput.value = response.path
          alert('완료')
          confirmBtn.classList.add('disabled')
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