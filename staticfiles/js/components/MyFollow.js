class MyFollow extends MainCards{
    _eventUserAuth (e) {
        super._eventUserAuth(e);
        if (this.target && this.target.name === 'subscribe') {
            this._eventSubscribe(this.target)
        }
    }

    _eventSubscribe  (target)  {
        const cardId = target.closest(this.card).getAttribute('data-id');
        if(target.hasAttribute('data-out')) {
            this.button.subscribe.addSubscribe(target,cardId)
        } else {
            this.button.subscribe.removeSubscribe(target,cardId)
        }
    }

}
