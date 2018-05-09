'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('django_migrations', {
    'app': {
      type: DataTypes.STRING,
    },
    'name': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'django_migrations',
    
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

