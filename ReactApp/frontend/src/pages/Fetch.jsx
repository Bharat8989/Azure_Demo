import { useState, useEffect } from "react";

function Fetch() {
  const [products, setProduct] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/products")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setProduct(data);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <>
      <h1>Product List</h1>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.name}
          </li>
        ))}
      </ul>
    </>
  );
}

export default Fetch;
