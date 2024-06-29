import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import RestaurantList from './components/RestaurantList';
import RestaurantDetail from './components/RestaurantDetail';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Zomato Restaurants</h1>
        
        <Switch>
          <Route exact path="/" component={RestaurantList} />
          <Route path="/restaurant/:id" component={RestaurantDetail} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;