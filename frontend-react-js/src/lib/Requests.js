import {getAccessToken} from 'lib/CheckAuth';

async function request(method,url,payload_data,setErrors,success){
  if (setErrors !== null){
    setErrors('')
  }
  let res
  try {
    await getAccessToken()
    const access_token = localStorage.getItem("access_token")
    const attrs = {
      method: method,
      headers: {
        'Authorization': `Bearer ${access_token}`,
        'Content-Type': 'application/json'
      }
    }

    if (method !== 'GET') {
      attrs.body = JSON.stringify(payload_data)
    }

    res = await fetch(url,attrs)
    let data = await res.json();
    if (res.status === 200) {
      success(data)
    } else {
      if (setErrors !== null){
        setErrors(data)
      }
      console.log(res,data)
    }
  } catch (err) {
    console.log('request catch',err)
    if (err instanceof Response) {
        console.log('HTTP error detected:', err.status); // Here you can see the status.
        if (setErrors !== null){
          setErrors([`generic_${err.status}`]) // Just an example. Adjust it to your needs.
        }
    } else {
      if (setErrors !== null){
        setErrors([`generic_500`]) // For network errors or any other errors
      }
    }
  }
}

export function post(url,payload_data,setErrors,success){
  request('POST',url,payload_data,setErrors,success)
}

export function put(url,payload_data,setErrors,success){
  request('PUT',url,payload_data,setErrors,success)
}

export function get(url,setErrors,success){
  request('GET',url,null,setErrors,success)
}

export function destroy(url,payload_data,setErrors,success){
  request('DELETE',url,payload_data,setErrors,success)
}