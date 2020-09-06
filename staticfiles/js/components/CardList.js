class CardList extends MainCards {
    _eventUserAuth (e) {
        super._eventUserAuth(e);
        if (this.target && this.target.name === 'purchpurchases') {
            this._eventPurchpurchases(this.target)
        }
        if (this.target && this.target.name === 'favorites') {
            this._eventFavorites(this.target);
        }
    }
    _eventUserNotAuth  (e)  {
        super._eventUserAuth(e);
        if (this.target && this.target.name === 'purchpurchases') {
            this._eventPurchpurchases(this.target)
        }
    }
    _eventFavorites  (target) {
        const cardId = target.closest(this.card).getAttribute('data-id');
        if(target.hasAttribute('data-out')) {
            this.button.favorites.addFavorites(target,cardId)
        } else {
            this.button.favorites.removeFavorites(target,cardId)
        }
    }
    _eventPurchpurchases  (target)  {
        const cardId = target.closest(this.card).getAttribute('data-id');
        if(target.hasAttribute('data-out')) {
            this.button.purchpurachases.addPurchases(target,cardId, this.counter.plusCounter)
        } else {
            this.button.purchpurachases.removePurchases(target,cardId,this.counter.minusCounter);

        }
    }
}
