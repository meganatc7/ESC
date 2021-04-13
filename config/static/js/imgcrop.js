// 필요한 각각의 태그들을 변수화
const imageBox = document.querySelector('#image-box')

const input = document.querySelector('#id_image')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const confirmBtn = document.querySelector('#confirm-btn')

// input변수에 이벤트
input.addEventListener('change', ()=>{
  console.log('changed')

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
    aspectRatio: 8 / 8,
    crop: function(event) {
      // console.log(event.detail.x);
      // console.log(event.detail.y);
      // console.log(event.detail.width);
      // console.log(event.detail.height);
      // console.log(event.detail.rotate);
      // console.log(event.detail.scaleX);
      // console.log(event.detail.scaleY);
    }
  });

  //여기서 부터 코드가 잘 이해가 안됩니다.
  var cropper = $image.data('cropper');

  confirmBtn.addEventListener('click', (event)=>{
    event.preventDefault()
    cropper.getCroppedCanvas().toBlob((blob)=>{
      console.log(blob)
      const signupForm = document.querySelector('#signup-form')
      const fd = new FormData(signupForm)
      // fd.append('csrfmiddlewaretoken', csrf[0].value)
      fd.set('image', blob, 'my-image.png')

      $.ajax({
        type: 'POST',
        url: signupForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(response){
          console.log(response)
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