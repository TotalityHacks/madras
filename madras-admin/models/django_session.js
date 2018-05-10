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
    'expire_date': {
      type: DataTypes.DATE,
    },
  }, {
    tableName: 'django_session',
    underscored: true,
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
  };

  return Model;
};

