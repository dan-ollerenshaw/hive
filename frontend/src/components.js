import React from 'react';
import { getDummy } from './api.js'
import cherry from './images/cherry-svgrepo-com.svg'
import lemon from './images/lemon-svgrepo-com.svg'
import orange from './images/orange-svgrepo-com.svg'
import watermelon from './images/watermelon-svgrepo-com.svg'

class PlayButton extends React.Component {
    handleClick = () => {
        var result = getDummy();
        console.log(result);
    };
    render() {
        return (
            <button onClick={this.handleClick} className="button-44">
                Play!
            </button>
        );
    }
}

class SlotMachineTable extends React.Component {
    render() {
        return (<div>
            <img src={cherry} width="50" height="50" />
            <img src={lemon} width="50" height="50" />
            <img src={orange} width="50" height="50" />
            <img src={watermelon} width="50" height="50" />
        </div>
        )
    }
}

export { PlayButton, SlotMachineTable }