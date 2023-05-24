import {ReactComponent as ReplyIcon} from './svg/reply.svg';

export default function ActivityActionReply(props) { 
  const onclick = (event) => {
    event.preventDefault()
    props.setReplyActivity(props.activity)
    props.setPopped(true)
    return false
  }

  let counter;
  if (props.count > 0) {
    counter = <div className="counter">{props.count}</div>;
  }

  return (
    <div onClick={onclick} className="action activity_action_reply">
      <ReplyIcon className='icon' />
      {counter}
    </div>
  )
}