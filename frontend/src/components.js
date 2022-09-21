import React from 'react';
import { getCashOut, postPlay } from './api.js'
import cherry from './images/cherry-svgrepo-com.svg'
import lemon from './images/lemon-svgrepo-com.svg'
import orange from './images/orange-svgrepo-com.svg'
import watermelon from './images/watermelon-svgrepo-com.svg'
import question from './images/question-mark-svgrepo-com.svg'


class SlotGame extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // TODO: put rolls in an array
            roll0: question,
            roll1: question,
            roll2: question,
            session_credit: 10,
            account_credit: 0,
            images: {
                "cherry": cherry,
                "lemon": lemon,
                "orange": orange,
                "watermelon": watermelon,
                "question": question
            },
            sessionID: null,
            block0_spinning: false,
            block1_spinning: false,
            block2_spinning: false,
            cashout_button_left_position: 800,
            cashout_button_disabled: false,
        };
    }

    // FIXME: why is this called twice?
    componentDidMount() {
        // send an initial request to obtain a session ID
        const sessionID = this.state.sessionID;
        fetch(
            'http://127.0.0.1:8000/session_id/',
            {
                method: 'GET',
            }
        ).then(response => {
            this.setState({ sessionID: response.headers.get('x-session-id') });
        })
    }

    handlePlayClick = () => {
        const sessionID = this.state.sessionID
        const images = this.state.images
        const account_credit = this.state.account_credit
        postPlay(sessionID, account_credit).then(
            result => {
                const roll = result['roll']
                const credit = result['session_credit']
                this.setState({
                    block0_spinning: true,
                    block1_spinning: true,
                    block2_spinning: true,
                })
                setTimeout(() => this.setState({ block0_spinning: false }), 1000);
                setTimeout(() => this.setState({ block1_spinning: false }), 2000);
                setTimeout(() => this.setState({ block2_spinning: false }), 3000);
                setTimeout(() => this.setState({ session_credit: credit }), 3000);
                this.setState({
                    // TODO: use loop here for rolls
                    roll0: images[roll[0]],
                    roll1: images[roll[1]],
                    roll2: images[roll[2]],
                    account_credit: 0
                })
            })
    }

    handleCashOutClick = () => {
        const sessionID = this.state.sessionID
        const account_credit = this.state.account_credit
        const cashout_button_disabled = this.state.cashout_button_disabled
        if (cashout_button_disabled) {
            console.log("disabled")
        } else {
            getCashOut(sessionID).then(result => {
                this.setState({
                    session_credit: 0,
                    account_credit: account_credit + result['account_credit']
                })
            })
        }
    }

    handleMouseOverCashOut = () => {
        const cashout_button_left_position = this.state.cashout_button_left_position
        let random_value = Math.random()
        if (random_value < 0.5) {
            // move 300px left or right
            let delta = 0
            if (random_value < 0.25) {
                delta = -300
            } else {
                delta = 300
            }
            let new_position = cashout_button_left_position + delta
            // ensure the button doesn't fly off the page completely
            let w = window.screen.width
            // https://stackoverflow.com/questions/4467539/javascript-modulo-gives-a-negative-result-for-negative-numbers
            new_position = ((new_position % w) + w) % w;
            this.setState({
                cashout_button_left_position: new_position,
                cashout_button_disabled: false
            })
        } else if (random_value < 0.9) {
            console.log("cashout disabled")
            this.setState({ cashout_button_disabled: true })
        } else {
            console.log("cashout button active!")
            this.setState({ cashout_button_disabled: false })
        }
    }


    render() {
        let cashout_button_left_position = this.state.cashout_button_left_position
        const rolls = [this.state.roll0, this.state.roll1, this.state.roll2]
        const session_credit = this.state.session_credit;
        const account_credit = this.state.account_credit;

        // TODO: this should be done in a loop
        let block0
        if (this.state.block0_spinning) {
            block0 = <img src={question} className="App-logo" height="100" weight="100" />
        } else {
            block0 = <Block src={rolls[0]} />
        }
        let block1
        if (this.state.block1_spinning) {
            block1 = <img src={question} className="App-logo" height="100" weight="100" />
        } else {
            block1 = <Block src={rolls[1]} />
        }
        let block2
        if (this.state.block2_spinning) {
            block2 = <img src={question} className="App-logo" height="100" weight="100" />
        } else {
            block2 = <Block src={rolls[2]} />
        }

        return (
            <div>
                <button onClick={this.handlePlayClick} className="button-44">
                    Play!
                </button>
                <br />
                {block0}
                {block1}
                {block2}
                <div>Session credit: {session_credit}</div>
                <div>Account credit: {account_credit}</div>
                <br />
                <button onClick={this.handleCashOutClick} className="button-44 green"
                    onMouseEnter={this.handleMouseOverCashOut}
                    style={{ position: 'fixed', bottom: 100, left: cashout_button_left_position, width: '20%' }}
                >
                    Cash out
                </button>
            </div >
        )
    }
}


class Block extends React.Component {
    render() {
        return (
            <img src={this.props.src} height="100" width="100"></img>
        )
    }
}

export { SlotGame }