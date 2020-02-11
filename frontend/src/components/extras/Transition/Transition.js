import React from 'react';
import arrow from './arrow.png';
import spinner from './spinner.svg';
import './Transition.css';

export class Transition extends React.Component {

    render() {
        let transitionImg;
        if (this.props.loading) {
            transitionImg = <img className="spinner" src={spinner} alt="spinner"></img>;
        } else {
            transitionImg = <img className="arrow" src={arrow} alt="arrow"></img>;
        }

        return (
            <div className="transition-div">
                {transitionImg}
            </div>
        );
    }
}
