'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('django_session', {
    'session_key': {
      type: DataTypes.STRING,
      primaryKey: true 
    },
    'session_data': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'django_session',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

