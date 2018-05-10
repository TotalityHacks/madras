'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('django_migrations', {
    'app': {
      type: DataTypes.STRING,
    },
    'name': {
      type: DataTypes.STRING,
    },
    'applied': {
      type: DataTypes.DATE,
    },
  }, {
    tableName: 'django_migrations',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
  };

  return Model;
};

