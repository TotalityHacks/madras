'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('registration_application', {
    'name': {
      type: DataTypes.STRING,
    },
    'status': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'registration_application',
    
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

