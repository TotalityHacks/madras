'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('director_organization', {
    'name': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'director_organization',
    
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

