import {BrowserRouter as Router,Route,Routes} from "react-router-dom"
import Home  from "./pages/Home"
import Fetch from "./pages/Fetch"
import Context from "./pages/Context"
import Props from "./pages/Props"
import Navbar from "./pages/Navbar"
import Profile from "./pages/Profile"
export const App = () => {
  const user={
    surname:"Kadam"

  };
  return (
    <>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} >
         {/* <Route path="/navbar" element={<Navbar />} /> */}

        </Route>
        {/* <Route path="/products" element={<Products />} /> */}
        <Route path="/fetch" element={<Fetch />} />
        <Route path="/context" element={<Context />} />
        <Route path='/props' element={<Props user={user} />} />
        <Route path="/navbar" element={<Navbar />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="*" element={<h1>404 Not Found</h1>}
         />
      </Routes>
    </Router>
  

     
    </>
  )
}
