likeBtn = document.querySelector('#like')
article = document.querySelector('#article')
csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

likeBtn.addEventListener('click',() => {
  console.log('좋아요')
  console.log(article.value)
  $.ajax({
    type: 'POST',
    url: '/articles/'+article.value+'/like/',
    data: {
      'pk': article.value,
      'csrfmiddlewaretoken': csrf,
    },
    dataType: 'json',
    success: function (response) {
      heart = document.querySelector('#heart')
      like_number = document.querySelector('#like-number')
      if (response.like == 0) {
        heart.style.color = ''
        heart.className = 'far fa-heart'
        console.log(response.like_number)
      } else {
        heart.style.color = 'tomato'
        heart.className = 'fas fa-heart'
        console.log(response.like_number)
      }
      console.log(like_number)
      like_number.innerText = `${response.like_number}명이 이 게시물을 좋아합니다.`
    },
    error: function () {

    },
  })
})