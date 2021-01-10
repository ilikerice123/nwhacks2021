import React from 'react'

export default class Recipe extends React.Component {
    constructor(props) {
        super(props)
        this.state = {recipe: null}
        this.recipeRef = React.createRef()
    }

    async componentDidUpdate(prevProps, prevState){
        if (prevProps.id != this.props.id && this.props.id != null) {
            let recipeId = this.props.id
            let res = await fetch(host() + 'transcribe?data=' + recipeId)
            this.props.stopLoading()
            if (!res.ok) {
                console.log('wtf why not ok')
                return
            }
            this.setState({recipe: await res.json()})
            this.recipeRef.current.scrollIntoView()
        }
    }

    render() {
        return (
            <div className={'recipe'} ref={this.recipeRef}>
                {this.state.recipe && 
                    <div className={'recipe-display'}>
                        <Ingredients ingredients={this.state.recipe.ingredients} />
                        <Instructions instructions={this.state.recipe.instructions} />
                    </div>
                }
            </div>
        )
    }
}

export function Ingredients(props) {
    let ingredients = props.ingredients
    return <div className="ingred">
        <h2>Ingredients</h2>
        <ul>
            {ingredients.map((ingred) => (
                <li>
                    {ingred}
                </li>
            ))}
        </ul>
    </div>
}

export function Instructions(props) {
    let instructions = props.instructions
    return <div className="ins">
        <h2>Instructions</h2>
        <ol>
            {instructions.map((instruction) => (
                <li>
                    {instruction.step}
                    {instruction.image && 
                        <div>
                            <br />
                            <img src={host() + instruction.image} />
                        </div>
                    }
                </li>
            ))}
        </ol>
    </div>
}

export function host() {
    let url = new URL(window.location.href)
    if (url.host.includes("localhost")) {
        return "http://localhost:5000/"
    } else {
        return "http://ec2-54-187-166-169.us-west-2.compute.amazonaws.com:4999/"
    }
}