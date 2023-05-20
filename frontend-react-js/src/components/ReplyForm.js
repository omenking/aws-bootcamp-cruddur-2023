import './ReplyForm.css';
import React from "react";
import process from 'process';
import {post} from 'lib/Requests';

import ActivityContent  from 'components/ActivityContent';
import FormErrors from 'components/FormErrors';

export default function ReplyForm(props) {
  const [count, setCount] = React.useState(0);
  const [message, setMessage] = React.useState('');
  const [errors, setErrors] = React.useState([]);

  const classes = []
  classes.push('count')
  if (240-count < 0){
    classes.push('err')
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/${props.activity.uuid}/reply`
    const payload_data = {
      activity_uuid: props.activity.uuid,
      message: message
    }
    post(url,payload_data,{
      auth: true,
      setErrors: setErrors,
      success: function(data){
        // add activity to the feed
        //let activities_deep_copy = JSON.parse(JSON.stringify(props.activities))
        //let found_activity = activities_deep_copy.find(function (element) {
        //  return element.uuid ===  props.activity.uuid;
        //});
        //found_activity.replies.push(data)
        //props.setActivities(activities_deep_copy);

        // reset and close the form
        setCount(0)
        setMessage('')
        props.setPopped(false)
      }
    })
  }

  const textarea_onchange = (event) => {
    setCount(event.target.value.length);
    setMessage(event.target.value);
  }

  let content;
  if (props.activity){
    content = <ActivityContent activity={props.activity} />;
  }

  const close = (event)=> {
    if (event.target.classList.contains("reply_popup")) {
      props.setPopped(false)
    }
  }
  if (props.popped === true) {
    return (
      <div className="popup_form_wrap reply_popup" onClick={close}>
        <div className="popup_form">
          <div className="popup_heading">
            <div className="popup_title">
              Reply to...
            </div>
          </div>
          <div className="popup_content">
            <div className="activity_wrap">
              {content}
            </div>
            <form 
              className='replies_form'
              onSubmit={onsubmit}
            >
              <textarea
                type="text"
                placeholder="what is your reply?"
                value={message}
                onChange={textarea_onchange} 
              />
              <div className='submit'>
                <div className={classes.join(' ')}>{240-count}</div>
                <button type='submit'>Reply</button>
              </div>
              <FormErrors errors={errors} />
            </form>
          </div>
        </div>
      </div>
    );
  }
}