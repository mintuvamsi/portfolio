import React, {Component} from "react";

class Welcome extends Component{
    render(){
        return <h2>Wlcome {this.props.name} a.k.a {this.props.heroName}</h2>
    }
}

export default Welcome