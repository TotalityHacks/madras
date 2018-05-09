'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('authtoken_token', {
    'key': {
      type: DataTypes.STRING,
      primaryKey: true 
    },
    'user_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'authtoken_token',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

