export default function doSomething() {

}

export const doSomething = () => {
    // Works better with call-back functions
    // Exports differently than function
}

// This is specific to React
const MyComponent = () => {
    return <div></div>
}

// In react this is actually recommended
<button 
    onClick={() => { 
        console.log("hello");
    }}>
</button>;

// Ternary Operators
//let age = 16;
//let name = age > 10 && "Pedro"; // If this condition is true, do this
//name = age > 16 || "Pedro"; // If this condition is not true, do this
//name = age > 10 ? "Pedro" : "Jack"; 
// If true, then Pedro, else Jack

// In react
const Component = () => {
    return age > 10 ? <div> Pedro </div> : <div> Jack</div>;

}

const name = "Pedro";

// Objects are very important in React
const person = {
    name,
    age: 20,
    isMarried: false,
};

// Instead of this
// const name = person.name;
// const age = person.age;
// const isMarried = person.isMarried

// const { name, age, isMarried } = person;