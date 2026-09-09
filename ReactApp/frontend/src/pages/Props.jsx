

export const Props = ({ user }) => {
    const user1={
        name:"Kadam"
    };
  return (
    <div>Props
    <h1>Hello {user1.name}</h1>
    <h2>Surname:{user.surname}</h2>
    </div>
  )
}


export default Props;