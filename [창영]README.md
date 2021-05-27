# ESC Project



## 01. 이메일 인증

> 회원가입 시 이메일을 활용한 본인 인증 기능



#### 1. 구글 계정 보안 수준 낮추기

장고 내에서 제공하는 mail 모듈을 사용하였다.

본격적으로 코드를 작성함에 앞서 몇가지 준비사항이 있다.

일단 나는 구글 메일을 사용했는데, 기본적인 흐름이 장고 서버에서 나의 구글 계정에 접근해서 이메일을 직접 발송하는 형태이다.

그렇기 때문에 구글 계정에서 `보안 수준이 낮은 앱의 액세스가 가능`하도록 설정해줘야한다.

즉, 보안 수준이 낮은 앱인 django가 구글 계정에 접근하도록 허용해 주는 것이다.



#### 2. settings.py에 계정 입력

보안 수준을 낮춰줬다면 장고에서 내 계정에 접근할 수 있도록 계정 정보를 입력해줘야한다.



```json
// secret.json

{
  "GOOGLE_ID": "계정",
  "GOOGLE_PW": "비밀번호!",
}
```

secret.json 파일을 하나 만들어서 구글 계정 정보를 입력해준다.(key값은 그냥 하고싶거 쓰면 된다.)



```python
# settings.py

# secret.json 불러오기
secret_file = os.path.join(BASE_DIR, 'secret.json')
with open(secret_file, 'r') as f:
    secrets = json.loads(f.read())

# 장고에 내 계정 정보 알려주기
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = secrets.get("GOOGLE_ID")
EMAIL_HOST_PASSWORD = secrets.get("GOOGLE_PW")
EMAIL_USE_TLS = True
```

그리고 settings.py에 작성한 secret.json을 불러와서 나의 계정 정보를 알려주면 된다.

settings.py에 바로 아이디와 비밀번호를 입력해줘도 되지만,

깃헙에 코드를 올린다면 settings.py에 나의 구글 계정 정보가 그대로 노출이 되니

secret.json에 따로 저장하고 해당 json파일은 깃헙에 안올라가게 해서 계정 노출을 해결한 것이다.



#### 3. 회원 모델 구축

위의 사전 작업이 끝났으면 이제 본격적으로 회원가입기능이다.

회원의 정보를 관리할 테이블을 만들기 위해 모델을 먼저 구축했다.

```python
# models.py

class User(AbstractUser):
    is_active = models.BooleanField(
        default=False,
    )
    email = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=300)
    nickname = models.CharField(max_length=100, unique=True)
    introduction = models.TextField()
    image = models.ImageField(upload_to='profile/%Y%m%d', null=True, blank=True)
    auth = models.CharField(max_length=20, blank=True)
    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
    )
```

모델은 장고에서 제공하는 User를 그대로 가져와서 사용했고,

인증을 위해 꼭 해줘야 할 작업은 is_active의 default값을 False로 생성하는 것이다.

회원가입 시 is_active가 False로 되어있으면 테이블에 회원 정보가 있더라도 로그인이 되질 않는다.

이걸 활용해서 이따가 이메일 인증을 통해 is_active를 True로 전환하여 로그인이 되도록 할 것이다.



#### 4. 회원가입 함수

만들었던 모델을 활용하여 CustomUserCreationForm이라는 model form을 미리 만들었다.

그리고 아래와 같이 회원가입을 하는 함수를 작성했다.

```python
# views.py

@require_http_methods(['GET','POST'])
def signup(request):
    # 로그인 되어있는 경우 인덱스 페이지로
    if request.user.is_authenticated:
        return redirect('articles:index')

    # POST 요청
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        # 유효성 검사
        if form.is_valid():
            user = form.save(commit=False)
            print(request.POST.get('cropped'))
            user.image = request.POST.get('cropped')
            user.save()
            # 유효성 검사 하고 난 뒤 이메일 보내기
            send_email(user.email)
            print('이메일 발송')
            return redirect('articles:index')
    # GET 요청
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```

다른 것들 보다 이메일 인증과 관련된 것을 살펴보고자 한다.

직접 만든 send_email함수를 사용했고 

send_email함수로 user의 email 정보를 인자로 보냈다.

바로 해당 함수를 살펴보자.



#### 5. 이메일 전송하는 함수



```python
# views.py

def send_email(email):
    url = f'http://127.0.0.1:8000/accounts/{email}/signin'
    html_content = render_to_string('accounts/email_template.html', {
        'url': url,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        #subject
        'ESC 이메일 인증',
        #content
        text_content,
        #from email
        settings.EMAIL_HOST_USER,
        #to
        [email],
    )

    email.attach_alternative(html_content,'text/html')
    email.send()
```

나는 이메일 인증 양식을 html로 만들어서 보내주고 싶었기 때문에

장고에서 제공하는 EmailMultiAlternatives를 사용했다.

EmailMultiAlternatives의 subclass인 EmailMessage의 attach_alternative 함수를 통해

다양한 것들을 이메일의 본문에 담아 보낼 수 있다. (여기서 내가 담을 것은 html 문서이다.)



이메일을 보낼 때 첫 줄의 url 링크를 같이 보내는데

첫 줄의 url을 통해 내가 만든 signin 함수로 요청이 가고, 그 함수를 통해 is_active를 True로 만들어 줄 것이다.



#### 6. is_active 바꾸기

코드는 정말 간단하다. 요청이 들어오면 해당 유저 객체를 찾아 is_active만 바꿔주면 된다.

```python
# views.py

@require_safe
def signin(request, email):
    # 해당 유저 객체를 받아온 뒤 is_active값을 1로 바꿔줌
    user = get_object_or_404(User, email=email)
    user.is_active = 1
    user.save()
    auth_login(request, user)
    return redirect('accounts:login')
```



이렇게만 해주면 이메일 인증 비슷무리한 기능을 만들어 볼 수 있다.





## 02. 이미지 크롭

> 회원가입 과정 에서 프로필 사진 설정 시 이미지 크롭할 수 있는 기능



#### 1. 크롭 기능 구현

일단은 먼저 이미지를 크롭하는 기능을 cropper.js 라이브러리를 사용해서 구현했다.

```js
// imgcrop.js

// 필요한 각각의 태그들을 변수화
const imageBox = document.querySelector('#image-box')
const input = document.querySelector('#id_image')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const confirmBtn = document.querySelector('#confirm-btn')


// input변수에 이벤트
input.addEventListener('change', ()=>{
  // input에 변화가 일어나면 confirmBtn이 나타나도록  
  confirmBtn.classList.remove('not-visible')

  //file 정보를 가져와서 img_data 변수에 저장
  const img_data = input.files[0]
  // Blob 객체를 나타내는 URL을 포함한 DOMString 생성
  const url = URL.createObjectURL(img_data)
  // 가져온 url로 imageBox에 고른 이미지 띄우기
  imageBox.innerHTML = `<img src="${url}" id="image" width="500px">`

  // jQuery로 이미지 태그 가져오기
  var $image = $('#image');

  // 이미지 크롭 기능(aspectRatio를 조정하여 크롭 비율 변경 가능)
  $image.cropper({
    aspectRatio: 9 / 9,
    crop: function(event) {

    }
  });
    
  // 크롭된 이미지 데이터 가져오기 
  var cropper = $image.data('cropper');

  confirmBtn.addEventListener('click', (event)=>{
    // 디폴트로 되어있는 버튼 기능을 먼저 막아주고(form 제출되는 기능들)
    event.preventDefault()
    // 크롭된 이미지를 blob객체로 만들고
    cropper.getCroppedCanvas().toBlob((blob)=>{
      console.log(blob)
      const fd = new FormData()
      // 해당 blob객체에 접근할 수 있는 url을 만들고
      const b_url = URL.createObjectURL(blob)
      
	  //폼 데이터에 하나하나 다 넣어줌
      fd.append('file', blob, 'my-image.png')
      fd.append('csrfmiddlewaretoken', csrf[0].value)
      fd.append('url', b_url)
      
	  // ajax를 통해 크롭한 이미지를 views.py에 있는 cropped 함수로 넘김
      $.ajax({
        type: 'POST',
        url: '/accounts/cropped/',
        // url: '{% url "accounts:cropped" %}',
        enctype: 'multipart/form-data',
        data: fd,
        dataType: 'json',
        success: function(response){
          // 성공하면 히든 인풋태그에 크롭된 이미지가 저장된 경로를 담아줌
          // 그리고 alert과 함께 확인 버튼을 비활성화
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
```

사실 javascript와 ajax를 처음 사용해 보았기에 cropper.js 사용하고 이해하는데 꽤나 시간이 오래 걸렸다.

여기서 blob이란 것도 처음 알게 되었는데, 일반 text로 된 데이터가 아닌 음성, 이미지, 동영상 등 용량이 큰 데이터들을 처리하기 위해 사용하는 객체라고 한다.

위 코드에선 blob을 통해 이미지 정보를 가진 객체를 만들고 createObjectURL로 url을 만들어 해당 이미지에 접근할 수 있도록 해준 것이다.



#### 2. 크롭된 사진 저장하기

위 js에서 크롭된 사진을 /accounts/cropped/ 경로로 보냈는데, 해당 url을 통해 아래와 같은 함수로 가게 된다.

```python
# views.py

def cropped(request):
    print('확인',request.POST, request.FILES)
    # request 객체에서 크롭된 이미지 데이터 꺼내기
    cropped = request.FILES.get('file')
    # 장고 서버 내부에 저장하고 해당 경로를 path 변수로 다시 넘겨줌
    path = default_storage.save(f'profile/{cropped.name}', cropped)
    return JsonResponse({'path':path})
```

ajax 송신으로 받은 request 객체에서 크롭된 이미지파일을 꺼내서 장고 서버 내에 해당 크롭된 이미지를 저장해주었다.

그리고 그 저장된 이미지의 경로를 다시 path에 담아 넘겨주었다.

그러면 위 js에서 그 path를 받아 hidden input태그에 이미지 파일을 담을 것이다.



#### 3. 회원가입 시 크롭된 이미지 저장

```python
# views.py

@require_http_methods(['GET','POST'])
def signup(request):
    # 로그인 되어있는 경우 인덱스 페이지로
    if request.user.is_authenticated:
        return redirect('articles:index')

    # POST 요청
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        # 유효성 검사
        if form.is_valid():
            # 정보만 넣어놓고 아직 저장은 하지 않도록 한 뒤
            user = form.save(commit=False)
            print(request.POST.get('cropped'))
            # image필드에 들어갈 데이터를 크롭된 이미지로 변경 한 뒤 저장
            user.image = request.POST.get('cropped')
            user.save()
            # 유효성 검사 하고 난 뒤 이메일 보내기
            send_email(user.email)
            print('이메일 발송')
            # return JsonResponse({'messgae': 'works'})
            return redirect('articles:index')
    # GET 요청
    else:
        form = CustomUserCreationForm()
    print('에러',form.errors)
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```

유효성 검사를 한 뒤 바로 저장하지 않고

user의 image필드에 들어갈 파일을 크롭된 이미지로 변경한 뒤 저장한다.

원래대로라면 크롭하기 이전인 전체 사진이 image필드에 저장이 되어야 정상이지만,

name속성이 cropped인 hidden input에 담겨있던 크롭된 이미지를 꺼내와서 바꾸준 것이다.



원래는 회원가입 화면에서 버튼을 1개로만 하여 그 버튼을 누르면 회원가입과 함께 크롭된 이미지로 저장되도록 구현하려고 했으나,,,

수많은 오류를 겪었고, 우여곡절 끝에 도달한 방법이 이 방법이었다.

크롭할 범위를 선정하고 '확인'버튼을 누르면 크롭된 이미지가 일시적으로 장고 서버 내부에 저장되고

회원가입 폼을 모두 작성한 뒤 제출할 때, 그때 저장될 이미지를 사용자가 입력값에 넣은 전체 이미지가 아닌 아까 장고 서버 내부에 저장한 크롭된 이미지로 바꿔치기 해주는 것이다.



## 02-1. 프로필 사진 수정(크롭 이미지)

> 프로필 사진 수정 시 크롭된 사진으로 저장되는 기능

전체적인 맥락은 회원가입때 했던 것과 똑같다.



#### 1. 크롭 기능 구현

```js
const profileBtn = document.querySelector('#chg-profile')
const profileBox = document.querySelector('#profile-box')

// 버튼을 눌르면
profileBtn.addEventListener('click', ()=>{

  const changeForm = document.querySelector('#chg-form')
  const confirmBtn = document.querySelector('#confirm-btn')
  // 이미지 수정할 수 있는 UI들이 보이도록 함
  changeForm.classList.remove('not-visible')
  confirmBtn.classList.remove('not-visible')

  const input = document.querySelector('#id_profile')
  const csrf = document.getElementsByName('csrfmiddlewaretoken')
  // 이미지를 선택해서 input에 넣으면
  input.addEventListener('change', ()=>{
    // 회원가입과 같은 크롭 기능
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
```

js는 회원가입때와 똑같다.

경로만 /accounts/update/profile/ 로 바꿔주었고 views.py의 updateprofile함수에서 데이터를 받아 처리를 할 것이다.



#### 2. 선택된 크롭 이미지로 수정

```python
@require_POST
def updateprofile(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        user.image = request.FILES.get('file')
        user.save()
        return JsonResponse({'message':'works'})
```

크롭된 이미지를 request 객체에서 꺼낸 뒤 유저의 image를 수정해준다.

회원가입때와 달리 굉장히 간단하게 구현했다.

잘 수정 했으면 응답으로 메시지를 보내주었다.



## 03. 비밀번호 찾기 기능

> 이메일로 보내진 인증번호를 통한 비밀번호 찾기 기능



#### 1. 패스워드 리셋 폼

장고에서 기본적으로 제공하는 PasswordResetForm을 사용했다.

```python
# forms.py

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        label = '회원가입 시 입력한 이메일을 입력해주세요.',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control mt-2',
            },
        )
    )
    class Meta(PasswordResetForm):
        model = get_user_model()
        fields = '__all__'


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label = '새 비밀번호',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
            },
        )
    )
    new_password2 = forms.CharField(
        label = '새 비밀번호 확인',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
            },
        )
    )
    class Meta(SetPasswordForm):
        model = get_user_model()
        fields = '__all__'
```

폼은 총 2개가 필요했다. 인증을 통해 패스워드를 리셋 시킬 폼과 

인증한 뒤 새로운 비밀번호로 바꿔줄 수 있는 폼이다.

즉, 리셋폼에서 입력받은 이메일로 인증번호를 보내고 해당 인증 번호를 맞게 사용자가 입력한다면

비밀번호를 정상적으로 리셋시켜줄 흐름으로 생각했다.



#### 2. 비밀번호 찾기 페이지

비밀번호 찾기 html 페이지는 크게 뭐가 있진 않다.

그냥 이메일을 입력받을 input과 확인버튼이다.

```django
// findpassword.html

<div class="mt-5">
    {% csrf_token %}
    {{ form }}
    <button class="btn btn-primary mt-3" id="find_pw">확인</button>
    <img src="{% static 'img/cube.gif' %}" alt="" class="mt-3 not-visible" width="50px" id="cube">
  </div>
  <div style="text-align: center; margin-top: 10px; margin-bottom: -10px;">
    <div id="loading"></div>
  </div>

  <div id="result_pw"></div>
```

이 정도의 느낌이고 이 페이지는 버튼을 누름에 따라 아래의 javascript를 통해

약간씩 바꿔주었다.

```js
// findpassword.html

<script type="text/javascript">
    $(document).ready(function () {
    // 이메일 입력한 뒤 확인 버튼을 누르면
      $('#find_pw').click(function () {
        // 확인 버튼 사라지고 로딩중인 이미지 뜨게하기
        $('#cube').removeClass('not-visible')
        $('#find_pw').addClass('not-visible')
        $('#loading').replaceWith('<div id="loading_end" class="loading"></div>')
        // email값을 가져오기(ajax로 넘길거임)
        var email = $('#id_email').val()
        
		// email을 json형태로해서 아래의 url로 넘김(해당 url에선 인증번호 메일을 전송함)
        $.ajax({
          type: 'POST',
          url: '/accounts/find_password/',
          dataType: 'json',
          data:{
            'email': email,
            'csrfmiddlewaretoken': '{{csrf_token}}',
          },
          success: function (response) {
            // 인증메일을 정상적으로 전송했으면 아래와 같이 태그들을 바꿔줌
            $('#loading_end').remove()
            $('#find_pw').remove()
            $('#cube').remove()
            alert('회원님의 이메일로 인증코드를 발송했습니다.')
            // 인증번호 입력란과 입력 후 누를 수 있는 버튼태그가 나오도록 해줌
            $('#result_pw').replaceWith(
                '<hr><div class="row justify-content-md-center"><form class="form-inline" style="margin-bottom:-15px; margin-top:-10px;"><div class="md-form md-outline"><label for="input_auth_num">인증번호 입력</label><input type="text" id="input_auth_num" class="form-control mx-sm-2" autofocus/></div></form>'+
                '<button type="submit" name="auth_confirm" id="id_auth_confirm" class="btn btn-red mt-3" style="opacity: 90%; height:30%; margin-top:10px; font-size: 12px;"><i class="fas fa-check"></i>&nbsp;&nbsp;인증확인</button></div><hr>'
            )
			// 인증번호 메일 전송 후 views에서 result에 username을 보냈는데,
            // 해당 username을 일단 받아옴(아래에서 사용할 것)
            var user = response.result
			
            $(document).ready(function () {
              // 사용자가 인증번호 입력한 뒤 인증번호 확인 버튼을 누르면
              $('#id_auth_confirm').click(function () {
                // 입력된 인증 번호를 일단 가져와서 ajax로 넘겨서 검증
                var input_auth_num = $('#input_auth_num').val()

                $.ajax({
                  type: 'POST',
                  url: '/accounts/pw/auth/',
                  dataType: 'json',
                  data: {
                    'user_id': user, // 위에서 받아온 username
                    'input_auth_num': input_auth_num, // 인증번호
                    'csrfmiddlewaretoken': '{{csrf_token}}',
                  },
                  success: function (response) {
                      // 통신이 잘 이뤄졌으면 resetpw 경로로 이동
                    location.href = "{% url 'accounts:resetpw' %}"
                  },
                  error: function () {
                      // 에러가 발생되면 아래와 같은 alert창 띄움
                    if ($('#input_auth_num').val() == ""){
                      alert('회원님의 이메일로 전송된 인증번호를 입력해주세요.')
                    } else {
                      alert('인증번호가 일치하지 않습니다.')
                    }
                  },
                })
              })
            })
          },
          error: function () {
              // 이메일을 잘못 입력하면 아래와 같은 alert띄움
            $('#find_pw').removeClass('not-visible')
            $('#cube').addClass('not-visible')
            $('#loading_end').remove()
            if (email == "") {
              alert('이메일을 입력해주세요.')
            } else {
              alert('입력하신 정보가 일치하지 않거나 존재하지 않습니다.')
            }
          }
        })
      })
    })
  </script>
```



#### 3. 인증번호 이메일 보내기

> js에서 첫번째 ajax

위 html문서와 js를 통해서 이메일을 입력하고 확인 버튼을 누르면

인증번호를 생성해서 보내는 함수가 실행된다.

```python
@require_http_methods(['GET','POST'])
def findpw(request):
    if request.method == 'POST':
        # request객체의 email을 통해 email객체 생성
        email = request.POST.get('email')
        # 해당 이메일로 유저 객체를 가져옴
        target_user = User.objects.get(email=email)
        print(target_user.username)
        # 잘 유저 객체를 뽑아왔으면
        if target_user:
            # 임의의 인증번호 생성
            string_pool = string.ascii_letters + string.digits
            auth_num = ""
            for _ in range(8):
                auth_num += random.choice(string_pool)
            
            # 유저의 auth 필드에 인증번호를 넣어줌(나중에 일치하는지 확인하기 위함)
            target_user.auth = auth_num
            target_user.save()
			
            # 이메일 보내기(여기선 html이 아닌 그냥 텍스트만 보내보았다.)
            send_mail(
                # title
                '비밀번호 찾기 인증메일입니다.',
                # content
                f'인증번호: {auth_num}',
                # from
                'meganatc7@gmail.com',
                # to
                [email],
            )
        # 위 로직을 정상적으로 실행했으면 유저이름을 response로 준다.
        return JsonResponse({'result': target_user.username})
    else:
        # GET요청인 경우에는 빈 폼(이메일 입력폼)을 그냥 담아 렌더링
        form = CustomPasswordResetForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/findpassword.html', context)
```

모델에는 auth라는 필드를 하나 만들어주었고 여기에 인증번호 생성 시

생성한 인증번호를 넣어주고 나중에 사용자가 인증번호를 입력하면

일치하는지 확인할 때 사용할 것이다.



#### 4. 인증번호 확인

>js에서 두번째 ajax

성공적으로 이메일 인증번호를 보냈다면

3번의 첫번 째 success함수를 통해 인증번호 입력 인풋 태그가 나타난다.

그리고 사용자가 해당 인풋 태그에 인증번호를 입력하고 확인 버튼을 누르면 검증을 한다.

```python
def authpw(request):
    # 이메일 보내면서 response로 보냈던 유저정보를 가져오고
    user_id = request.POST.get('user_id')
    # 유저가 입력한 인증번호도 가져오고
    input_auth_num = request.POST.get('input_auth_num')
    # 그걸 토대로 유저 객체 생성
    target_user = User.objects.get(username=user_id, auth=input_auth_num)
    # auth를 빈 문자열로 바꿔주고
    target_user.auth = ""
    target_user.save()
    # 세션에 유저이름을 저장해둠
    request.session['auth'] = target_user.username

    return JsonResponse({'result': target_user.username})
```



#### 5. 비밀번호 변경

사용자가 인증번호를 맞게 입력했다면 success함수를 통해 비밀번호를 리셋할 수 있는

페이지로 이동하게 해주었다.

실패한다면? error함수를 통해 alert을 띄운다.

```django
// password_rest.html

<form action="" method="POST">
    {% csrf_token %}
    {{ form }}
    <button class="btn btn-primary mt-3">확인</button>
  </form>
```

비밀번호 리셋하는 페이지에도 마찬가지로 별 내용은 없다.

form에서 만들었던 CustomSetPasswordForm을  띄우고 데이터를 받아와서 변경해주면 된다.



```python
# views.py
@require_http_methods(['GET','POST'])
def resetpw(request):
    if request.method == 'POST':
        # 세션에 저장해두었던 유저네임을 꺼내와서
        session_user = request.session['auth']
        # 그걸 기반으로 유저 객체를 만들고
        current_user = User.objects.get(username=session_user)
		
        # 폼에서 입력값을 받아오고
        reset_password_form = CustomSetPasswordForm(current_user, request.POST)
	
    	# 유효성 검사 한 뒤에 바뀐 비밀번호 저장
        if reset_password_form.is_valid():
            user = reset_password_form.save()
            messages.success(request, '비밀번호 변경 완료!')
            # 로그인 페이지로 이동
            return redirect('accounts:login')
        else:
            auth_logout(request)
            # request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)
    context = {
        'form': reset_password_form,
    }
    return render(request, 'accounts/password_reset.html', context)
```

사용자가 바꿀 비밀번호를 입력하면 이전에 세션값으로 저장해두었던 유저네임을 활용하여 유저 객체

를 가져오고 해당 유저의 비밀번호를 새롭게 갱신한다.

이런 식으로 비밀번호 찾기 기능을 구현해보았다.