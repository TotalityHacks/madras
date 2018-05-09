'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('auth_group', {
    'name': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'auth_group',
    
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

